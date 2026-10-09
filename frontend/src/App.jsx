
import { useEffect, useMemo, useState } from "react";
import "./App.css";

const SAVED_JOBS_KEY = "hirehunt_saved_jobs";

function App() {
  const [role, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [keywords, setKeywords] = useState("");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sortBy, setSortBy] = useState("match");
  const [verifiedOnly, setVerifiedOnly] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [savedJobs, setSavedJobs] = useState([]);
  const [showSaved, setShowSaved] = useState(false);

  useEffect(() => {
    try {
      const storedJobs = localStorage.getItem(SAVED_JOBS_KEY);
      if (storedJobs) {
        const parsedJobs = JSON.parse(storedJobs);
        if (Array.isArray(parsedJobs)) setSavedJobs(parsedJobs);
      }
    } catch {
      localStorage.removeItem(SAVED_JOBS_KEY);
    }
  }, []);

  const toggleSaveJob = (job) => {
    const alreadySaved = savedJobs.some(
      (savedJob) => savedJob.job_url === job.job_url
    );

    const updatedJobs = alreadySaved
      ? savedJobs.filter((savedJob) => savedJob.job_url !== job.job_url)
      : [...savedJobs, job];

    setSavedJobs(updatedJobs);
    localStorage.setItem(SAVED_JOBS_KEY, JSON.stringify(updatedJobs));
  };

  const findJobs = async (event) => {
    event?.preventDefault();

    if (!role.trim() || !location.trim() || !keywords.trim()) {
      setError("Please fill in your role, location and skills.");
      return;
    }

    setLoading(true);
    setError("");
    setJobs([]);
    setShowSaved(false);

    try {
      const apiBaseUrl = (
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

const response = await fetch(`${apiBaseUrl}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: role.trim(),
          location: location.trim(),
          keywords: keywords.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error("The job search request failed.");
      }

      const data = await response.json();
      setJobs(Array.isArray(data.jobs) ? data.jobs : []);
    } catch {
      setError(
        "Unable to connect to HireHunt. Please check that your FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const displayedJobs = useMemo(() => {
    const sourceJobs = showSaved ? savedJobs : jobs;
    let filteredJobs = [...sourceJobs];

    if (verifiedOnly) {
      filteredJobs = filteredJobs.filter(
        (job) => job.url_status === "verified"
      );
    }

    if (sortBy === "match") {
      filteredJobs.sort(
        (a, b) => (b.match_score || 0) - (a.match_score || 0)
      );
    } else if (sortBy === "company") {
      filteredJobs.sort((a, b) =>
        (a.company || "").localeCompare(b.company || "")
      );
    }

    return filteredJobs;
  }, [jobs, savedJobs, showSaved, sortBy, verifiedOnly]);

  const verifiedCount = jobs.filter(
    (job) => job.url_status === "verified"
  ).length;

  const averageMatch = jobs.length
    ? Math.round(
        jobs.reduce((sum, job) => sum + (job.match_score || 0), 0) /
          jobs.length
      )
    : 0;

  const scrollToSearch = () => {
    document.getElementById("job-search")?.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
    document.getElementById("role-input")?.focus({ preventScroll: true });
  };

  return (
    <div className="app">
      <header className="navbar">
        <a
          href="#home"
          className="logo"
          aria-label="HireHunt AI home"
          onClick={() => {
            setShowSaved(false);
            setSelectedJob(null);
          }}
        >
          <span className="logo-mark">H</span>
          <span>HireHunt</span>
          <span className="ai-text">AI</span>
        </a>

        <nav className="nav-actions" aria-label="Main navigation">
          <button
            className="saved-count"
            onClick={() => {
              setShowSaved(true);
              document.getElementById("dashboard")?.scrollIntoView({
                behavior: "smooth",
              });
            }}
          >
            Saved jobs <strong>{savedJobs.length}</strong>
          </button>

          <div className="status">
            <span className="status-dot" />
            AI JOB MATCHING
          </div>
        </nav>
      </header>

      <main id="home">
        <section className="hero">
          <div className="badge">LIVE AI JOB DISCOVERY</div>

          <h1>
            Your next opportunity.
            <br />
            <span>One smart search away.</span>
          </h1>

          <p className="subtitle">
            Discover relevant job opportunities with AI-powered matching.
            Spend less time searching and more time preparing for your next role.
          </p>

          <form id="job-search" className="search-panel" onSubmit={findJobs}>
            <div className="input-group">
              <label htmlFor="role-input">JOB ROLE</label>
              <input
                id="role-input"
                type="text"
                placeholder="e.g. Software Engineer Intern"
                value={role}
                onChange={(event) => setRole(event.target.value)}
              />
            </div>

            <div className="input-group">
              <label htmlFor="location-input">LOCATION</label>
              <input
                id="location-input"
                type="text"
                placeholder="e.g. Delhi NCR or Remote"
                value={location}
                onChange={(event) => setLocation(event.target.value)}
              />
            </div>

            <div className="input-group">
              <label htmlFor="keywords-input">SKILLS / KEYWORDS</label>
              <input
                id="keywords-input"
                type="text"
                placeholder="e.g. Python, AI, FastAPI"
                value={keywords}
                onChange={(event) => setKeywords(event.target.value)}
              />
            </div>

            <button className="search-button" type="submit" disabled={loading}>
              {loading ? "SEARCHING..." : "Find jobs  →"}
            </button>
          </form>

          {error && <p className="error-message">{error}</p>}

          <div className="hero-trust">
            <span>AI-powered discovery</span>
            <span>Personalised matches</span>
            <span>Direct application links</span>
          </div>
        </section>

        <section className="dashboard" id="dashboard">
          <div className="dashboard-heading">
            <div>
              <p className="section-label">YOUR CAREER WORKSPACE</p>
              <h2>
                {showSaved ? "Your saved jobs" : "Explore opportunities"}
              </h2>
              <p className="dashboard-subtitle">
                {showSaved
                  ? "Keep track of roles you want to revisit."
                  : "Your job search, organised in one place."}
              </p>
            </div>

            <button
              className="reset-view-button"
              onClick={() => {
                setShowSaved(false);
                setVerifiedOnly(false);
                setSortBy("match");
              }}
            >
              All opportunities
            </button>
          </div>

          <div className="stats-grid">
            <article className="stat-card">
              <div className="stat-icon purple-icon">J</div>
              <div>
                <p>Total opportunities</p>
                <strong>{jobs.length}</strong>
                <span>From your latest search</span>
              </div>
            </article>

            <article className="stat-card">
              <div className="stat-icon green-icon">V</div>
              <div>
                <p>Verified links</p>
                <strong>{verifiedCount}</strong>
                <span>Among latest results</span>
              </div>
            </article>

            <article className="stat-card">
              <div className="stat-icon blue-icon">%</div>
              <div>
                <p>Average match</p>
                <strong>{averageMatch}%</strong>
                <span>Based on latest results</span>
              </div>
            </article>

            <article className="stat-card">
              <div className="stat-icon amber-icon">S</div>
              <div>
                <p>Saved jobs</p>
                <strong>{savedJobs.length}</strong>
                <span>Stored in this browser</span>
              </div>
            </article>
          </div>

          {loading && (
            <div className="loading-section">
              <div className="loader" />
              <h3>Finding your next opportunity...</h3>
              <p>
                HireHunt is searching for relevant roles. This may take a
                little while.
              </p>
            </div>
          )}

          {!loading && (
            <>
              <div className="results-header">
                <div>
                  <p className="section-label">
                    {showSaved ? "YOUR COLLECTION" : "JOB DISCOVERIES"}
                  </p>
                  <h2>
                    {displayedJobs.length}{" "}
                    {displayedJobs.length === 1
                      ? "opportunity"
                      : "opportunities"}
                  </h2>
                </div>

                <div className="result-controls">
                  <select
                    aria-label="Sort jobs"
                    value={sortBy}
                    onChange={(event) => setSortBy(event.target.value)}
                  >
                    <option value="match">Best match</option>
                    <option value="company">Company A-Z</option>
                  </select>

                  <label className="verified-filter">
                    <input
                      type="checkbox"
                      checked={verifiedOnly}
                      onChange={(event) =>
                        setVerifiedOnly(event.target.checked)
                      }
                    />
                    Verified only
                  </label>
                </div>
              </div>

              {displayedJobs.length > 0 ? (
                <div className="jobs-grid">
                  {displayedJobs.map((job, index) => {
                    const isSaved = savedJobs.some(
                      (savedJob) => savedJob.job_url === job.job_url
                    );

                    return (
                      <article
                        className="job-card"
                        key={job.job_url || `${job.title}-${index}`}
                      >
                        <div className="job-top">
                          <div className="company-icon">
                            {(job.company || "J").charAt(0).toUpperCase()}
                          </div>

                          <div className="match-score">
                            <strong>{job.match_score ?? 0}%</strong>
                            <span>MATCH</span>
                          </div>
                        </div>

                        <h3>{job.title || "Untitled opportunity"}</h3>
                        <p className="company-name">
                          {job.company || "Company not specified"}
                        </p>

                        <div className="job-location">
                          {job.location || "Location not specified"}
                        </div>

                        <div className="job-source">
                          <span
                            className={
                              job.url_status === "verified"
                                ? "verified"
                                : "not-verified"
                            }
                          >
                            {job.url_status === "verified"
                              ? "VERIFIED LINK"
                              : "UNVERIFIED LINK"}
                          </span>
                          <span>{job.source || "Job source"}</span>
                        </div>

                        {job.match_reasons?.length > 0 && (
                          <div className="match-reasons">
                            {job.match_reasons.map((reason, reasonIndex) => (
                              <div className="match-reason" key={reasonIndex}>
                                <span>✓</span>
                                {reason}
                              </div>
                            ))}
                          </div>
                        )}

                        {job.short_description && (
                          <p className="description">
                            {job.short_description}
                          </p>
                        )}

                        <button
                          className="details-button"
                          onClick={() => setSelectedJob(job)}
                        >
                          View details
                        </button>

                        <button
                          className="save-button"
                          onClick={() => toggleSaveJob(job)}
                        >
                          {isSaved ? "★ Saved" : "☆ Save job"}
                        </button>

                        {job.job_url && (
                          <a
                            href={job.job_url}
                            target="_blank"
                            rel="noreferrer"
                            className="apply-button"
                          >
                            Apply now ↗
                          </a>
                        )}
                      </article>
                    );
                  })}
                </div>
              ) : (
                <div className="empty-state">
                  <div className="empty-state-icon">
                    {showSaved ? "☆" : "⌕"}
                  </div>
                  <h3>
                    {showSaved
                      ? "No saved jobs yet"
                      : jobs.length > 0
                        ? "No jobs match these filters"
                        : "Your next role starts here"}
                  </h3>
                  <p>
                    {showSaved
                      ? "Save interesting opportunities from your search and find them here."
                      : jobs.length > 0
                        ? "Try turning off Verified only or changing the sort and filters."
                        : "Enter your preferred role, location and skills above to discover opportunities."}
                  </p>
                  {showSaved ? (
                    <button
                      className="empty-action"
                      onClick={() => setShowSaved(false)}
                    >
                      Explore opportunities
                    </button>
                  ) : jobs.length === 0 ? (
                    <button className="empty-action" onClick={scrollToSearch}>
                      Start a job search
                    </button>
                  ) : null}
                </div>
              )}
            </>
          )}
        </section>
      </main>

      {selectedJob && (
        <div
          className="modal-overlay"
          onClick={() => setSelectedJob(null)}
        >
          <section
            className="job-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="job-modal-title"
            onClick={(event) => event.stopPropagation()}
          >
            <button
              className="close-modal"
              aria-label="Close job details"
              onClick={() => setSelectedJob(null)}
            >
              ×
            </button>

            <div className="modal-icon">
              {(selectedJob.company || "J").charAt(0).toUpperCase()}
            </div>

            <h2 id="job-modal-title">
              {selectedJob.title || "Job details"}
            </h2>
            <p className="modal-company">
              {selectedJob.company || "Company not specified"}
            </p>

            <div className="modal-meta">
              <span>{selectedJob.location || "Location not specified"}</span>
              <span>{selectedJob.source || "Job source"}</span>
            </div>

            <div className="modal-match">
              <strong>{selectedJob.match_score ?? 0}%</strong>
              <span>MATCH SCORE</span>
            </div>

            <div className="modal-section">
              <h3>WHY THIS MATCHES</h3>
              {selectedJob.match_reasons?.length ? (
                selectedJob.match_reasons.map((reason, index) => (
                  <div className="modal-reason" key={index}>
                    <span>✓</span>
                    {reason}
                  </div>
                ))
              ) : (
                <p>No match explanation is available for this role.</p>
              )}
            </div>

            <div className="modal-section">
              <h3>ABOUT THIS ROLE</h3>
              <p>
                {selectedJob.short_description ||
                  "No description available for this position."}
              </p>
            </div>

            {selectedJob.job_url && (
              <a
                href={selectedJob.job_url}
                target="_blank"
                rel="noreferrer"
                className="modal-apply"
              >
                Apply for this role ↗
              </a>
            )}
          </section>
        </div>
      )}

      <footer>
        <span>HireHunt AI</span>
        <span>Less searching. Better matches.</span>
      </footer>
    </div>
  );
}

export default App;