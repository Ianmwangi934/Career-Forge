import "./ResumeManager.css";
import { useState, useEffect } from "react";
import axios from "axios";

const ResumeManager = () => {
    const [file, setFile] = useState(null)
    const [title, setTitle] = useState("")
    const [resumes, setResumes] = useState([])
    const [loading, setLoading] = useState(false)

    // Fetch resumes
    const fetchResumes = async () => {
        try {
            const res = await axios.get(
                "http://localhost:8000/resumes/",
                {withCredentials: true}
            )
            setResumes(res.data)

        } catch (err) {
            console.error("Error fetching resumes", err)
        }
    }

    useEffect(() => {
        fetchResumes()
    }, [])

    // Upload Resumes
    const handleUpload = async (e) => {
        e.preventDefault()

        if (!file) {
            alert ("Please Select a File")
            return
        }

        const formData = new FormData()
        formData.append("file", file)
        formData.append("title", title)

        try {
            setLoading(true)
            await axios.post(
                "http://localhost:8000/resumes/upload/",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    },
                    withCredentials:true
                }
            )
            setFile(null)
            setTitle("")
            fetchResumes()
        } catch (err) {
            console.error("Upload failed", err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="resume-manager">

      {/* UPLOAD FORM */}
      <form onSubmit={handleUpload} className="upload-box">

        <h2>Upload Resume</h2>

        <input
          type="text"
          placeholder="Optional title (e.g. Backend Resume)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Uploading..." : "Upload"}
        </button>

      </form>

      {/* LIST */}
      <div className="resume-list">

        <h2>Your Resumes</h2>

        {resumes.length === 0 ? (
          <div className="empty-state">
                <h3>No resumes yet</h3>
                <p>
                    Upload your first resume to start tailoring your career strategy with precision.
                </p>
            </div>
        ) : (
          resumes.map((resume) => (
            <div key={resume.id} className="resume-item">
              <p>
                {resume.title || resume.file.split("/").pop()}
              </p>
              <span>
                {new Date(resume.uploaded_at).toLocaleDateString()}
              </span>
            </div>
          ))
        )}

      </div>

    </div>
    )
}
export default ResumeManager;