# HireHunt AI 🔍

**Your AI-powered job search assistant.**

HireHunt AI helps users discover relevant job opportunities based on their preferred role, location, and keywords. It collects job listings, removes duplicates, and presents organized results with job details and application links.

## ✨ Features

* 🔎 Search for jobs using roles, locations, and keywords
* 🤖 AI-powered job discovery using TinyFish
* 🔗 Direct application links to job postings
* 🧹 Deduplicated and structured job results
* 🎯 Relevant job matches with explanations
* ↕️ Filter and sort job listings
* 💾 Save jobs for later
* 📋 View job details in an interactive interface

## 🛠️ Tech Stack

**Frontend**

* React
* Vite
* CSS

**Backend**

* Python
* FastAPI
* TinyFish API

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/ektajain7217/HireHunt-AI.git
cd HireHunt-AI
```

### 2. Set up the Python backend

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies required by the project.

### 3. Configure environment variables

Create a `.env` file in the project root and add your TinyFish API key:

```env
TINYFISH_API_KEY=your_tinyfish_api_key
```

Replace the placeholder with your own API key. Never commit your actual `.env` file or expose your API key publicly.

### 4. Start the backend

```bash
uvicorn main:app --reload
```

### 5. Set up the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your terminal.

## 🔐 Security

Keep API keys and other secrets in environment variables. The `.env` file is excluded from Git using `.gitignore`.

## 🚀 Future Improvements

* Deploy the frontend and backend
* Add user authentication
* Improve job recommendations
* Add more job sources and advanced search filters

## 👩‍💻 Author

**Ekta Jain**

* GitHub: [@ektajain7217](https://github.com/ektajain7217)

---

*Built to make job discovery smarter and easier.*
