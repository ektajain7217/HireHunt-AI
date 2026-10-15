# HireHunt AI — AI-Powered Job & Internship Finder

**Discover live opportunities. Find better matches. Apply smarter.**

HireHunt AI is a full-stack, TinyFish-powered job and internship discovery platform that helps users find relevant opportunities based on their preferred roles, locations, and skills.

Instead of manually searching multiple job portals, users can discover live openings through a single interface, review ranked results, analyze skill matches, save opportunities, and access application links.

🌐 **Live Demo:** https://hire-hunt-ai.vercel.app/

💻 **GitHub Repository:** https://github.com/ektajain7217/HireHunt-AI

## Key Features

- Live job and internship discovery using TinyFish Search, Fetch, and Agent
- Personalized searches by job role, location, and keywords
- Discovery across multiple job portals and company career pages
- Extraction of job details from individual career listings
- Structured results with job titles, companies, locations, and application URLs
- Duplicate job detection and removal
- Relevance scoring and job ranking
- Skill-match analysis and personalized improvement suggestions
- Job URL verification powered by TinyFish Agent
- Filtering, sorting, and saved jobs
- Responsive React frontend

## How TinyFish Is Integrated

HireHunt AI integrates **three TinyFish endpoints** through the official Python SDK.

### 1. TinyFish Search — Job Discovery

**Endpoint:** `client.search.query()`

TinyFish Search discovers relevant job posting URLs based on the user's preferences.

The application:

- Builds a search query using the requested role, location, and keywords.
- Searches for relevant career and internship opportunities.
- Filters discovered URLs to supported career-page domains.
- Excludes general company careers pages and direct application-form URLs.
- Selects candidate job pages for further processing.

### 2. TinyFish Fetch — Job Information Extraction

**Endpoint:** `client.fetch.get_contents()`

TinyFish Fetch retrieves the content of job pages discovered through Search.

The application:

- Fetches the selected job pages.
- Reads available job titles, descriptions, and location information.
- Parses supported individual job listings into structured records.
- Excludes pages without sufficient information or matching locations.
- Produces job records that can be combined with Agent results.

### 3. TinyFish Agent — Live Job Discovery and Verification

**Endpoint:** `client.agent.run()`

TinyFish Agent performs goal-driven job discovery across live web sources.

The application:

- Provides Agent with the user's role, location, and keyword preferences.
- Requests structured job information from discovered listings.
- Retrieves job titles, companies, locations, descriptions, and URLs.
- Uses additional Agent calls to verify selected job links.

Agent discovery runs independently of Search and Fetch, allowing its results to remain available even when Search and Fetch do not identify additional valid listings.

## End-to-End Architecture

**User enters role, location, and keywords**

↓

**FastAPI backend receives the search request**

↓

**TinyFish Search** discovers candidate job URLs

↓

**TinyFish Fetch** retrieves selected job-page content

↓

**Python parser** extracts valid, location-matching job listings

↓

**TinyFish Agent** independently discovers additional live opportunities

↓

**Backend combines Search + Fetch and Agent results**

↓

**Deduplication, relevance ranking, and skill analysis**

↓

**TinyFish Agent verifies selected job URLs**

↓

**React frontend displays the results**

## Job Processing and Ranking

After retrieving the results, HireHunt AI performs several processing steps:

**Structured extraction:** Converts discovered listings into consistent records containing job title, company, location, source, description, and application URL.

**Deduplication:** Removes duplicate job listings using normalized URLs.

**Relevance ranking:** Scores opportunities based on the user's requested role, location, and keywords.

**Skill analysis:** Highlights matching skills, skills not mentioned in a listing, and suggested areas for improvement.

**URL verification:** Uses TinyFish Agent to inspect selected job links and provide verification status.

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, CSS |
| Backend | Python, FastAPI |
| Live Web Discovery | TinyFish Search |
| Job Page Extraction | TinyFish Fetch |
| Agentic Automation | TinyFish Agent |
| Deployment | Vercel, Render |
| Version Control | Git, GitHub |

## Installation and Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ektajain7217/HireHunt-AI.git
cd HireHunt-AI
```

### 2. Create a Python Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure TinyFish

Create a `.env` file in the project root:

```env
TINYFISH_API_KEY=your_tinyfish_api_key
```

**Security:** Never commit the `.env` file or API keys to GitHub.

### 5. Start the FastAPI Backend

```bash
uvicorn main:app --reload
```

### 6. Start the React Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local development URL displayed by Vite.

## Working Demo

**Live Application:** https://hire-hunt-ai.vercel.app/

### Example Search

- **Role:** Software Engineer Intern
- **Location:** India
- **Keywords:** Python, React

The application discovers relevant job opportunities, combines available results, removes duplicates, and displays ranked listings with skill insights and application links.

### Integration Test Results

During local testing, HireHunt AI successfully demonstrated:

| Metric | Observed Result |
|---|---|
| TinyFish Search | 3 candidate job URLs |
| TinyFish Fetch | 3 job pages retrieved |
| Search + Fetch | 1 valid India-based listing |
| TinyFish Agent | 12 discovered listings |
| Combined Results | 13 listings before deduplication |
| Final Results | 12 unique listings |

These figures represent one observed test run. Results may vary as live job listings and search responses change.

The updated backend has also been deployed on Render and tested through the live Vercel frontend.

## TinyFish Technical Student Bounty

Built for **TinyFish Technical Student Bounty — Drop 001: Job Portal / Careers Finder**.

The project demonstrates:

- Meaningful integration of TinyFish Search, Fetch, and Agent
- Live job discovery from multiple sources
- User-controlled search preferences
- Structured job listings with application links
- Duplicate detection and relevance ranking
- Skill insights and job link verification
- A deployed, working full-stack application

## Author

**Ekta Jain**

GitHub: https://github.com/ektajain7217

---

*HireHunt AI — Making job discovery smarter, faster, and more accessible.*