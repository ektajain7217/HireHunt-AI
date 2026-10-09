import os
from dotenv import load_dotenv
from tinyfish import TinyFish

load_dotenv()

if not os.getenv("TINYFISH_API_KEY"):
    raise RuntimeError("TinyFish API key not found in .env")

client = TinyFish()


def find_jobs(role, location, keywords):
    goal = f"""
You are the live job discovery engine for HireHunt AI.

Find current job and internship listings matching:

Role: {role}
Location: {location}
Keywords: {keywords}

Search across multiple job sources and company career pages.

For every genuine listing, return:

- title
- company
- location
- source
- job_url
- short_description

IMPORTANT:
- Only return listings that you actually discover.
- Do not invent companies, jobs, URLs, or descriptions.
- Avoid duplicate listings.
- Prefer direct application URLs.
- If a direct application URL cannot be confirmed, use the discovered job URL.
- Make sure each job has a URL.

Return ONLY valid JSON in this exact format:

[
    {{
        "title": "Job title",
        "company": "Company name",
        "location": "Job location",
        "source": "Source website",
        "job_url": "https://...",
        "short_description": "Short description"
    }}
]
"""

    print("Searching live jobs...")

    response = client.agent.run(
        url="https://www.google.com",
        goal=goal
    )

    return response


def clean_jobs(response):
    """
    Convert TinyFish response into clean HireHunt data.
    """

    try:
        raw_result = response.result

        if isinstance(raw_result, dict):
            jobs = raw_result.get("result", raw_result)
        else:
            jobs = raw_result

        if not isinstance(jobs, list):
            return []

        cleaned = []
        seen_urls = []

        for job in jobs:

            if not isinstance(job, dict):
                continue

            title = str(job.get("title", "")).strip()
            company = str(job.get("company", "")).strip()
            location = str(job.get("location", "")).strip()
            source = str(job.get("source", "")).strip()
            url = str(job.get("job_url", "")).strip()
            description = str(
                job.get("short_description", "")
            ).strip()

            if not title or not company or not url:
                continue

            normalized_url = url.lower().rstrip("/")

            if normalized_url in seen_urls:
                continue

            seen_urls.append(normalized_url)

            cleaned.append({
                "title": title,
                "company": company,
                "location": location,
                "source": source,
                "job_url": url,
                "short_description": description
            })

        return cleaned

    except Exception as error:
        print("Could not process TinyFish response.")
        print("Error:", error)
        return []


def calculate_match_score(job, role, location, keywords):
    """
    Give every job a relevance score from 0 to 100.

    Role       = 40 points
    Location   = 30 points
    Keywords   = 30 points
    """

    score = 0
    reasons = []

    job_title = job["title"].lower()
    job_location = job["location"].lower()
    job_description = job["short_description"].lower()

    role_text = role.lower().strip()
    location_text = location.lower().strip()

    searchable_text = (
        job_title + " " + job_description
    )

    # -------------------------
    # 1. ROLE MATCH - 40 points
    # -------------------------

    if role_text and role_text in searchable_text:
        score += 40
        reasons.append("Strong role match")
    else:
        role_words = role_text.split()

        matched_role_words = 0

        for word in role_words:
            if len(word) > 2 and word in searchable_text:
                matched_role_words += 1

        if matched_role_words > 0:
            role_score = min(
                40,
                matched_role_words * 15
            )

            score += role_score
            reasons.append("Partial role match")

    # -------------------------
    # 2. LOCATION MATCH - 30 points
    # -------------------------

    if location_text and location_text in job_location:
        score += 30
        reasons.append("Location match")
    else:
        location_words = location_text.split()

        location_matched = False

        for word in location_words:
            if len(word) > 2 and word in job_location:
                location_matched = True
                break

        if location_matched:
            score += 20
            reasons.append("Related location")

    # -------------------------
    # 3. KEYWORDS - 30 points
    # -------------------------

    keyword_list = []

    for keyword in keywords.split(","):
        keyword = keyword.strip().lower()

        if keyword:
            keyword_list.append(keyword)

    if len(keyword_list) > 0:

        matched_keywords = 0

        for keyword in keyword_list:
            if keyword in searchable_text:
                matched_keywords += 1

        keyword_score = int(
            (matched_keywords / len(keyword_list)) * 30
        )

        score += keyword_score

        if matched_keywords > 0:
            reasons.append(
                f"{matched_keywords}/{len(keyword_list)} keywords matched"
            )

    return min(score, 100), reasons


def rank_jobs(jobs, role, location, keywords):
    """
    Add match score to every job and sort
    from highest match to lowest match.
    """

    ranked_jobs = []

    for job in jobs:

        score, reasons = calculate_match_score(
            job,
            role,
            location,
            keywords
        )

        job["match_score"] = score
        job["match_reasons"] = reasons

        ranked_jobs.append(job)

    ranked_jobs = sorted(
        ranked_jobs,
        key=lambda job: job["match_score"],
        reverse=True
    )

    return ranked_jobs

def verify_job_url(job):
    """
    Use TinyFish Agent to verify whether the job URL
    actually belongs to the discovered job.
    """

    goal = f"""
Verify this job listing page for HireHunt AI.

Job title: {job["title"]}
Company: {job["company"]}
Expected location: {job["location"]}

Open the following URL:

{job["job_url"]}

Check whether the page appears to be a genuine job listing
for the expected company and job title.

Return ONLY valid JSON in this exact format:

{{
    "verified": true,
    "reason": "The page matches the company and job title."
}}

Rules:

- verified must be true or false.
- Do not guess.
- If the page is unavailable, broken, unrelated, or clearly
  belongs to another job, return false.
- Keep the reason short.
"""

    try:
        response = client.agent.run(
            url=job["job_url"],
            goal=goal
        )

        raw_result = response.result

        if isinstance(raw_result, dict):
            result = raw_result.get("result", raw_result)
        else:
            result = raw_result

        if isinstance(result, dict):
            verified = bool(result.get("verified", False))
            reason = str(
                result.get("reason", "")
            ).strip()

            return verified, reason

    except Exception as error:
        print(
            f"URL verification failed for {job['company']}: "
            f"{error}"
        )

    return False, "Could not verify this URL."


if __name__ == "__main__":

    role = "Software Engineer Intern"
    location = "Delhi NCR"
    keywords = "Python, AI"

    response = find_jobs(
        role=role,
        location=location,
        keywords=keywords
    )

    jobs = clean_jobs(response)

    ranked_jobs = rank_jobs(
        jobs,
        role,
        location,
        keywords
    )

    # -------------------------
    # VERIFY TOP 5 JOB URLS
    # -------------------------

    print("\nVerifying top job URLs...")

    jobs_to_verify = min(5, len(ranked_jobs))

    for index in range(jobs_to_verify):

        job = ranked_jobs[index]

        print(
            f"Checking {index + 1}/{jobs_to_verify}: "
            f"{job['company']} - {job['title']}"
        )

        verified, reason = verify_job_url(job)

        job["url_verified"] = verified
        job["verification_reason"] = reason

    # -------------------------
    # FINAL RESULTS
    # -------------------------

    print("\n========== HIREHUNT AI ==========")
    print(f"Found {len(ranked_jobs)} unique jobs\n")

    for number, job in enumerate(ranked_jobs, start=1):

        print(f"{number}. {job['title']}")
        print(f"   Match Score: {job['match_score']}/100")

        if job.get("url_verified"):
            print("   URL Status: VERIFIED")
        else:
            print("   URL Status: NOT VERIFIED")

        print(
            f"   Verification: "
            f"{job.get('verification_reason', 'Not checked')}"
        )

        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")
        print(f"   Apply: {job['job_url']}")

        print(
            f"   Why: {', '.join(job['match_reasons'])}"
        )

        print(
            f"   Description: "
            f"{job['short_description']}"
        )

        print()