import os
from dotenv import load_dotenv
from tinyfish import TinyFish
from urllib.parse import urlparse
from types import SimpleNamespace

load_dotenv()

if not os.getenv("TINYFISH_API_KEY"):
    raise RuntimeError("TinyFish API key not found in .env")

client = TinyFish()
def search_and_fetch_jobs(role, location, keywords):
    """
    Discover job postings with TinyFish Search
    and read their content with TinyFish Fetch.
    """
    print("TinyFish Search: Discovering job postings...")

    try:
        search_query = (
            f'{role} jobs internships {location} {keywords} '
            'Lever Ashby Greenhouse careers apply'
        )

        search_response = client.search.query(
            query=search_query,
            purpose="Find individual job postings matching user preferences"
        )

        urls = []

        for result in search_response.results:
            url = str(result.url or "").strip()

            if not url.startswith("https://"):
                continue

            if not any(domain in url for domain in [
                "jobs.lever.co/",
                "jobs.ashbyhq.com/",
                "boards.greenhouse.io/"
            ]):
                continue
            from urllib.parse import urlparse

            parsed_url = urlparse(url)
            path_parts = [
                part for part in parsed_url.path.split("/")
                if part
            ]

            # Skip general company careers pages
            if len(path_parts) < 2:
                continue

            # Skip direct application forms
            if path_parts[-1].lower() == "apply":
                continue
            if url not in urls:
                urls.append(url)

            if len(urls) == 3:
                break

        if not urls:
            print("No suitable individual job URLs found.")
            return []

        print(f"TinyFish Search found {len(urls)} URLs.")
        print("TinyFish Fetch: Reading job descriptions...")

        fetch_response = client.fetch.get_contents(
            urls=urls,
            purpose="Read job titles, locations, descriptions and requirements"
        )

        fetched_jobs = []

        for page in fetch_response.results:
            content = str(page.text or "").strip()

            if len(content) < 150:
                continue

            fetched_jobs.append({
                "url": str(page.final_url or page.url),
                "title": str(page.title or ""),
                "content": content[:4000]
            })

        print(f"TinyFish Fetch read {len(fetched_jobs)} pages.")

        return fetched_jobs

    except Exception as error:
        print(f"Search/Fetch failed: {error}")
        return []

def parse_fetched_jobs(fetched_jobs, requested_location):
    """
    Convert fetched Ashby/Lever job pages into structured listings.
    Skip listings with missing or mismatched locations.
    """
    parsed_jobs = []

    for page in fetched_jobs:
        url = page.get("url", "")
        content = page.get("content", "")
        title = page.get("title", "").strip()

        if not url or not title or not content:
            continue

        parsed_url = urlparse(url)
        hostname = (parsed_url.hostname or "").lower()
        path_parts = [
            part for part in parsed_url.path.split("/") if part
        ]

        if hostname not in ("jobs.ashbyhq.com", "jobs.lever.co"):
            continue

        if len(path_parts) < 2:
            continue

        company = path_parts[0].replace("-", " ").title()

        lines = [line.strip() for line in content.splitlines()]

        location = ""

        if hostname == "jobs.ashbyhq.com":
            for index, line in enumerate(lines):
                if line.lower() == "## location":
                    for next_line in lines[index + 1:]:
                        if next_line:
                            location = next_line
                            break
                    break

        elif hostname == "jobs.lever.co":
            for line in lines:
                if line and not line.startswith("#"):
                    location = line
                    break

        if not location:
            continue

        requested = requested_location.strip().lower()

        if requested == "india":
            india_terms = [
                "india", "bengaluru", "bangalore",
                "delhi", "mumbai", "pune", "hyderabad",
                "chennai", "gurugram", "gurgaon",
                "noida", "kolkata", "ahmedabad"
            ]

            if not any(term in location.lower() for term in india_terms):
                continue

        elif requested and requested not in location.lower():
            continue

        description = " ".join(
            line for line in lines
            if line and not line.startswith("#")
        )[:1200]

        parsed_jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "source": hostname,
            "job_url": url,
            "short_description": description
        })

    return parsed_jobs
def find_jobs(role, location, keywords):
    fetched_jobs = search_and_fetch_jobs(role, location, keywords)
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

    # Extract jobs discovered by TinyFish Agent
    agent_jobs = []

    if response.result is not None:
        raw_result = response.result

        if isinstance(raw_result, dict):
            agent_jobs = raw_result.get("result", [])
        elif isinstance(raw_result, list):
            agent_jobs = raw_result

    if not isinstance(agent_jobs, list):
        agent_jobs = []

        # Convert fetched job pages into structured listings
    parsed_jobs = parse_fetched_jobs(fetched_jobs, location)

    # Combine Agent and Search + Fetch results
    combined_jobs = agent_jobs + parsed_jobs

    print(f"Agent returned {len(agent_jobs)} jobs.")
    print(f"Search + Fetch returned {len(parsed_jobs)} valid jobs.")
    print(f"Combined jobs before deduplication: {len(combined_jobs)}")

    # Preserve the response format expected by clean_jobs()
    return SimpleNamespace(result={"result": combined_jobs})


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


def analyze_job_skills(job, keywords):
    """
    Compare requested skills with the available job description.
    Skills not found are described as not mentioned, not definitively missing.
    """

    description = (
        str(job.get("title", "")) + " " +
        str(job.get("short_description", ""))
    ).lower()

    requested_skills = [
        skill.strip()
        for skill in str(keywords or "").split(",")
        if skill.strip()
    ]

    matched_skills = []
    not_mentioned_skills = []

    for skill in requested_skills:
        if skill.lower() in description:
            matched_skills.append(skill)
        else:
            not_mentioned_skills.append(skill)

    suggestions = []

    if not_mentioned_skills:
        suggestions.append(
            "Review the job description or contact the employer to confirm "
            "whether these skills are required: "
            + ", ".join(not_mentioned_skills)
            + "."
        )

    if matched_skills:
        suggestions.append(
            "Highlight relevant projects or experience demonstrating: "
            + ", ".join(matched_skills)
            + "."
        )

    if not requested_skills:
        suggestions.append(
            "Add skills to your search preferences for more detailed analysis."
        )

    return {
        "matched_skills": matched_skills,
        "skills_not_mentioned": not_mentioned_skills,
        "skill_analysis_note": (
            "Analysis is based on the available job title and short description. "
            "A skill not mentioned here is not necessarily a skill you lack."
        ),
        "improvement_suggestions": suggestions
    }


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

        # Add explainable skill analysis
        skill_analysis = analyze_job_skills(job, keywords)
        job.update(skill_analysis)

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
