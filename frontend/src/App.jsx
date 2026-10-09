import { useEffect, useMemo, useState } from "react";
import "./App.css";

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

  useEffect(() => {
  const storedJobs = localStorage.getItem("hirehunt_saved_jobs");

  if (storedJobs) {
    setSavedJobs(JSON.parse(storedJobs));
  }
}, []);

const toggleSaveJob = (job) => {
  const alreadySaved = savedJobs.some(
    (savedJob) => savedJob.job_url === job.job_url
  );

  let updatedJobs;

  if (alreadySaved) {
    updatedJobs = savedJobs.filter(
      (savedJob) => savedJob.job_url !== job.job_url
    );
  } else {
    updatedJobs = [...savedJobs, job];
  }

  setSavedJobs(updatedJobs);

  localStorage.setItem(
    "hirehunt_saved_jobs",
    JSON.stringify(updatedJobs)
  );
};
  const findJobs = async () => {
    if (!role || !location || !keywords) {
      setError("Please fill in all the fields.");
      return;
    }

    setLoading(true);
    setError("");
    setJobs([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          role: role,
          location: location,
          keywords: keywords,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch jobs.");
      }

      const data = await response.json();
      setJobs(data.jobs || []);
    } catch (err) {
      setError(
        "Unable to connect to HireHunt backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const displayedJobs = useMemo(() => {
  let filteredJobs = [...jobs];

  if (verifiedOnly) {
    filteredJobs = filteredJobs.filter(
      (job) => job.url_status === "verified"
    );
  }

  if (sortBy === "match") {
    filteredJobs.sort(
      (a, b) => (b.match_score || 0) - (a.match_score || 0)
    );
  }

  if (sortBy === "company") {
    filteredJobs.sort((a, b) =>
      (a.company || "").localeCompare(b.company || "")
    );
  }

  return filteredJobs;
}, [jobs, sortBy, verifiedOnly]);

  return (
    <div className="app">
      <div className="background-glow glow-one"></div>
      <div className="background-glow glow-two"></div>

      <header className="navbar">
        <div className="logo">
          <span className="logo-mark">H</span>
          <span>HireHunt</span>
          <span className="ai-text">AI</span>
        </div>

        <div className="nav-actions">
  <div className="saved-count">
    ★ {savedJobs.length} SAVED
  </div>

  <div className="status">
    <span className="status-dot"></span>
    AI JOB MATCHING
  </div>
</div>
      </header>

      <main>
        <section className="hero">
          <div className="badge">✦ LIVE AI JOB DISCOVERY</div>

          <h1>
            Find jobs.
            <br />
            <span>Not endless searches.</span>
          </h1>

          <p className="subtitle">
            Tell HireHunt what you're looking for. Our AI discovers live
            opportunities and finds the best matches for you.
          </p>

          <div className="search-panel">
            <div className="input-group">
              <label>ROLE</label>
              <input
                type="text"
                placeholder="e.g. Software Engineer Intern"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>LOCATION</label>
              <input
                type="text"
                placeholder="e.g. Delhi NCR"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>SKILLS / KEYWORDS</label>
              <input
                type="text"
                placeholder="e.g. Python, AI, FastAPI"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
              />
            </div>

            <button className="search-button" onClick={findJobs}>
              {loading ? "SEARCHING..." : "FIND MY JOBS →"}
            </button>
          </div>

          {error && <p className="error-message">{error}</p>}
        </section>

        {loading && (
          <section className="loading-section">
            <div className="loader"></div>
            <h3>HireHunt is searching the web...</h3>
            <p>Finding live opportunities and verifying the best matches.</p>
          </section>
        )}

        {!loading && jobs.length > 0 && (
          <section className="results-section">
            <div className="results-header">
              <div>
                <p className="section-label">YOUR RESULTS</p>
                <h2>{jobs.length} opportunities found</h2>
              </div>

              <div className="result-controls">
  <select
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value)}
  >
    <option value="match">Best Match</option>
    <option value="company">Company A–Z</option>
  </select>

  <label className="verified-filter">
    <input
      type="checkbox"
      checked={verifiedOnly}
      onChange={(e) => setVerifiedOnly(e.target.checked)}
    />
    Verified Only
  </label>
</div>
            </div>

            <div className="jobs-grid">
              {displayedJobs.map((job, index) => (
                <div className="job-card" key={index}>
                  <div className="job-top">
                    <div className="company-icon">
                      {job.company?.charAt(0) || "J"}
                    </div>

                    <div className="match-score">
                      <strong>{job.match_score}%</strong>
                      <span>MATCH</span>
                    </div>
                  </div>

                  <h3>{job.title}</h3>

                  <p className="company-name">
                    {job.company}
                  </p>

                  <div className="job-location">
                    📍 {job.location || "Location not specified"}
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
                        ? "✓ VERIFIED"
                        : "○ NOT VERIFIED"}
                    </span>

                    <span>{job.source}</span>
                  </div>
{job.match_reasons && job.match_reasons.length > 0 && (
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
<button
  className="save-button"
  onClick={() => toggleSaveJob(job)}
>
  {savedJobs.some(
    (savedJob) => savedJob.job_url === job.job_url
  )
    ? "★ SAVED"
    : "☆ SAVE JOB"}
</button>
  VIEW DETAILS
</button>
                  <a
                    href={job.job_url}
                    target="_blank"
                    rel="noreferrer"
                    className="apply-button"
                  >
                    APPLY NOW ↗
                  </a>
                </div>
              ))}
            </div>
          </section>
        )}
        {selectedJob && (
  <div
    className="modal-overlay"
    onClick={() => setSelectedJob(null)}
  >
    <div
      className="job-modal"
      onClick={(e) => e.stopPropagation()}
    >
      <button
        className="close-modal"
        onClick={() => setSelectedJob(null)}
      >
        ×
      </button>

      <div className="modal-icon">
        {selectedJob.company?.charAt(0) || "J"}
      </div>

      <h2>{selectedJob.title}</h2>

      <p className="modal-company">
        {selectedJob.company}
      </p>

      <div className="modal-meta">
        <span>
          📍 {selectedJob.location || "Location not specified"}
        </span>

        <span>
          🔗 {selectedJob.source}
        </span>
      </div>

      <div className="modal-match">
        <strong>{selectedJob.match_score}%</strong>
        <span>MATCH SCORE</span>
      </div>

      <div className="modal-section">
        <h3>WHY THIS MATCHES</h3>

        {selectedJob.match_reasons?.map(
          (reason, index) => (
            <div className="modal-reason" key={index}>
              <span>✓</span>
              {reason}
            </div>
          )
        )}
      </div>

      <div className="modal-section">
        <h3>ABOUT THIS ROLE</h3>

        <p>
          {selectedJob.short_description ||
            "No description available for this position."}
        </p>
      </div>

      <a
        href={selectedJob.job_url}
        target="_blank"
        rel="noreferrer"
        className="modal-apply"
      >
        APPLY NOW ↗
      </a>
    </div>
  </div>
)}
      </main>

      <footer>
        <span>HireHunt AI</span>
        <span>Less searching. Better matches.</span>
      </footer>
    </div>
  );
}

export default App;