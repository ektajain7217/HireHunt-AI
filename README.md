# HireHunt AI — AI-Powered Job & Internship Finder

**Discover live opportunities. Find better matches. Apply smarter.**

HireHunt AI is a TinyFish-powered job and internship discovery platform that helps users find relevant openings based on their preferred roles, locations, and keywords.

Instead of manually browsing multiple career portals, users can search for opportunities through a single interface, review ranked results, explore skill matches, and access application links.

🌐 **Live Demo:** https://hire-hunt-ai.vercel.app/

💻 **GitHub:** https://github.com/ektajain7217/HireHunt-AI

## Features

- Live job and internship discovery powered by TinyFish Agent
- Customizable searches by role, location, and keywords
- Discovery across multiple job sources and career pages
- Structured job listings with application links
- Duplicate job detection and removal
- Job relevance scores and matching explanations
- Matched skills and skills-not-mentioned analysis
- Personalized skill improvement suggestions
- Job URL verification using TinyFish Agent
- Job filtering, sorting, and saved jobs
- Responsive React interface

## How TinyFish Is Used

HireHunt AI uses the TinyFish Python SDK to interact with the live web.

**1. Live Job Discovery**

The backend calls `client.agent.run()` with a search goal based on the user's preferences. TinyFish Agent navigates live web sources to discover relevant job opportunities.

**2. Job Link Verification**

The backend also uses `client.agent.run()` to visit discovered job URLs and check whether they correspond to the expected job listings.

**3. Processing and Ranking**

After receiving TinyFish results, the Python backend structures the data, removes duplicates, calculates relevance scores, and generates skill-match insights.

The application currently uses the TinyFish Agent interface for these operations. Separate TinyFish Search and Fetch API integrations are not claimed.

## Tech Stack

**Frontend:** React, Vite, CSS

**Backend:** Python, FastAPI

**Web Automation:** TinyFish Python SDK

**Deployment:** Vercel (frontend), Render (backend)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ektajain7217/HireHunt-AI.git
cd HireHunt-AI
```

### 2. Set Up the Backend

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure TinyFish

Create a `.env` file in the project root:

```env
TINYFISH_API_KEY=your_tinyfish_api_key
```

Never commit API keys or the `.env` file to GitHub.

### 4. Start the Backend

```bash
uvicorn main:app --reload
```

### 5. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite.

## Working Demo

Try different roles, locations, and keywords to discover live opportunities.

The application processes job results and provides matching scores, skill insights, and application links.

**Live Application:** https://hire-hunt-ai.vercel.app/

## TinyFish Student Bounty

Built for **Technical Student Bounty Drop 001 — Job Portal / Careers Finder**.

The project demonstrates TinyFish-powered live job discovery, structured results, duplicate removal, job ranking, and application link verification.

## Author

**Ekta Jain**

GitHub: https://github.com/ektajain7217

---

*HireHunt AI — Making job discovery smarter, faster, and more accessible.*