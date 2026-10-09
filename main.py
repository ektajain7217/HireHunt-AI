from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from job_finder import (
    find_jobs,
    clean_jobs,
    rank_jobs,
    verify_job_url
)


app = FastAPI(
    title="HireHunt AI",
    description="AI-powered live job discovery and matching system",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JobSearchRequest(BaseModel):
    role: str
    location: str
    keywords: str


@app.get("/")
def home():
    return {
        "message": "Welcome to HireHunt AI",
        "status": "running"
    }


@app.post("/search")
def search_jobs(request: JobSearchRequest):

    print("\n==============================")
    print("HIREHUNT AI SEARCH")
    print("==============================")

    print(f"Role: {request.role}")
    print(f"Location: {request.location}")
    print(f"Keywords: {request.keywords}")

    # -------------------------
    # 1. LIVE JOB DISCOVERY
    # -------------------------

    response = find_jobs(
        role=request.role,
        location=request.location,
        keywords=request.keywords
    )

    # -------------------------
    # 2. CLEAN RESULTS
    # -------------------------

    jobs = clean_jobs(response)

    # -------------------------
    # 3. MATCH SCORING
    # -------------------------

    ranked_jobs = rank_jobs(
        jobs,
        request.role,
        request.location,
        request.keywords
    )

    # -------------------------
    # 4. VERIFY TOP 5 URLS
    # -------------------------

    jobs_to_verify = min(
        5,
        len(ranked_jobs)
    )

    for index in range(jobs_to_verify):

        job = ranked_jobs[index]

        print(
            f"Verifying {index + 1}/{jobs_to_verify}: "
            f"{job['company']} - {job['title']}"
        )

        verified, reason = verify_job_url(job)

        job["url_status"] = (
            "verified"
            if verified
            else "invalid"
        )

        job["verification_reason"] = reason

    # -------------------------
    # 5. MARK REMAINING JOBS
    # -------------------------

    for index in range(jobs_to_verify, len(ranked_jobs)):

        ranked_jobs[index]["url_status"] = "not_checked"

        ranked_jobs[index]["verification_reason"] = (
            "URL verification has not been performed yet."
        )

    # -------------------------
    # 6. RETURN RESULTS
    # -------------------------

    return {
        "success": True,
        "preferences": {
            "role": request.role,
            "location": request.location,
            "keywords": request.keywords
        },
        "total_jobs": len(ranked_jobs),
        "jobs": ranked_jobs
    }