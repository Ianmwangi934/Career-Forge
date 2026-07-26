import "./Dashboard.css"
import { useEffect, useState } from "react"
import axios from "axios"
import ResumeManager from "./ResumeManager";
import JobTargetForm from "./JobTargetForm";
import AIQuestionCard from "./AIQuestionCard";
import Applications from "./Applications";

const Dashboard = () => {
  const [user, setUser] = useState(null)
  const [activeSection, setActiveSection] = useState("dashboard")
  const [careerNews, setCareerNews] = useState([])

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await axios.get(
          "http://80.225.78.96/accounts/me/",
          { withCredentials: true }
        )
        setUser(res.data)
      } catch (err) {
        console.error(err)
      }
    }
    // Fetching career Insights and market trends

    const fetchCareerNews = async () => {
      try {
        const res = await axios.get(
          "http://80.225.78.96/ai_engine/career-news/"
        )

        setCareerNews(res.data)
      } catch (err) {
        console.error(err)
      }
    }
    fetchUser()
    fetchCareerNews()
  }, [])

  return (
    <div className="dashboard">

      {/* SIDEBAR */}
      <aside className="sidebar">
        <h2 className="logo">CareerForge</h2>

        <nav className="nav">
          <button
            className={`nav-item ${activeSection === "dashboard" ? "active" : ""}`}
            onClick={() => setActiveSection("dashboard")}
          >
            Home
          </button>

          <button
            className={`nav-item ${activeSection === "resumes" ? "active" : ""}`}
            onClick={() => setActiveSection("resumes")}
          >
            Resumes
          </button>

          <button
            className={`nav-item ${
              activeSection === "applications"
                ? "active"
                : ""
            }`}
            onClick={() => setActiveSection("applications")}
          >
            Applications
          </button>

          <button
            className={`nav-item ${activeSection === "ai" ? "active" : ""}`}
            onClick={() => setActiveSection("ai")}
          >
            AI Tools
          </button>
        </nav>

        <div className="sidebar-footer">
          <p>{user ? user.username : "User"}</p>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main">

        {/* HEADER */}
        <div className="topbar">
          <h1>
            Welcome back{user ? `, ${user.username}` : ""} 
          </h1>
        </div>

        {/* CONTENT */}
        <div className="content">

          {activeSection === "dashboard" && (
            <>
              <div className="intro-card">
                <h2>Career Overview</h2>
                <p>
                  Manage resumes, prepare for interviews,
                  track applications, and stay informed
                  about industry trends.
                </p>
              </div>

              <div className="cards">
                <div className="card">
                  <h3> Resumes</h3>
                  <p>Upload and tailor resumes for each job.</p>
                  <button onClick={() => setActiveSection("resumes")}>
                    Manage Resumes
                  </button>
                </div>

                <div className="card">
                  <h3> Applications</h3>
                  <p>Track your job applications and progress.</p>
                  <button onClick={() => setActiveSection("applications")}>View Applications</button>
                </div>

                <div className="card">
                  <h3> AI Tools</h3>
                  <p>Generate resumes, cover letters, and prep.</p>
                  <button onClick={() => setActiveSection("ai")}>Use AI</button>
                </div>


              </div>
              <div className="career-news-section">

                  <h2 className="career-news-title">
                    Career News
                  </h2>

                  <div className="news-slider">

                    <div className="news-track">

                      {[...careerNews, ...careerNews].map(
                        (news, index) => (

                          <a
                            key={index}
                            href={news.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="news-card"
                          >

                            {
                              news.image && (
                                <img
                                  src={news.image}
                                  alt={news.title}
                                />
                              )
                            }

                            <div className="news-content">

                              <span className="news-source">
                                {news.source}
                              </span>

                              <h3>
                                {news.title}
                              </h3>

                              <p>
                                {news.description}
                              </p>

                            </div>

                          </a>

                        )
                      )}

                    </div>

                  </div>

                </div>
            </>
          )}

          {activeSection === "resumes" && <ResumeManager />}
          {activeSection === "ai" && <JobTargetForm />}
          {activeSection === "aiquestions" && <AIQuestionCard />}
          {activeSection === "applications" && (<Applications />)}
          


        </div>

      </main>
    </div>
  )
}

export default Dashboard