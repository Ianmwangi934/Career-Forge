import "./Dashboard.css"
import { useEffect, useState } from "react"
import axios from "axios"

const Dashboard = () => {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await axios.get(
          "http://127.0.0.1:8000/accounts/me/",
          { withCredentials: true }
        )
        setUser(res.data)
      } catch (err) {
        console.error(err)
      }
    }

    fetchUser()
  }, [])

  return (
    <div className="dashboard">

      {/* SIDEBAR */}
      <aside className="sidebar">
        <h2 className="logo">CareerForge</h2>

        <nav className="nav">
          <button className="nav-item active">Dashboard</button>
          <button className="nav-item">Resumes</button>
          <button className="nav-item">Applications</button>
          <button className="nav-item">AI Tools</button>
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
            Welcome back{user ? `, ${user.username}` : ""} 👋
          </h1>
        </div>

        {/* CONTENT */}
        <div className="content">

          <div className="intro-card">
            <h2>Shape your career intentionally</h2>
            <p>
              CareerForge helps you tailor your career strategy with precision — 
              from optimized resumes to interview mastery.
            </p>
          </div>

          <div className="cards">

            <div className="card">
              <h3>📄 Resumes</h3>
              <p>Upload and tailor resumes for each job.</p>
              <button>Manage Resumes</button>
            </div>

            <div className="card">
              <h3>📊 Applications</h3>
              <p>Track your job applications and progress.</p>
              <button>View Applications</button>
            </div>

            <div className="card">
              <h3>🧠 AI Tools</h3>
              <p>Generate resumes, cover letters, and prep.</p>
              <button>Use AI</button>
            </div>

          </div>

        </div>

      </main>
    </div>
  )
}

export default Dashboard