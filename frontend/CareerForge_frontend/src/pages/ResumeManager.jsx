import "./ResumeManager.css";
import { useState, useEffect } from "react";
import axios from "axios";
import { Document, Page, pdfjs } from "react-pdf";
import workerSrc from "pdfjs-dist/build/pdf.worker?url";
pdfjs.GlobalWorkerOptions.workerSrc = workerSrc


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
    const handleDelete = async (id) => {
      try {
        await axios.delete(
          `http://localhost:8000/resumes/${id}/delete/`,
          {withCredentials:true}
        )
        fetchResumes()
      } catch (err) {
        console.error("Delete failed:", err)
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

              <div className="preview">
                {(() => {
                  if (!resume.file) return <p>No file</p>

                  const fileUrl = resume.file.startsWith("http")
                    ? resume.file
                    : `http://localhost:8000${resume.file}`

                  if (!fileUrl.endsWith(".pdf")) {
                    return <p>Preview not available</p>
                  }

                  return (
                    <a href={fileUrl} target="_blank" rel="noopener noreferrer">
                      <Document
                        file={fileUrl}
                        onLoadError={(err) => console.error("PDF load error:", err)}
                      >
                        <Page pageNumber={1} width={150} />
                      </Document>
                    </a>
                  )
                })()}
              </div>

              <div className="resume-info">
                <p>{resume.title || resume.file.split("/").pop()}</p>
                <span>
                  {new Date(resume.uploaded_at).toLocaleDateString()}
                </span>

                {/* 🔥 NEW ACTIONS */}
                <div className="resume-actions">

                  <a
                    href={`http://localhost:8000${resume.file}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="view-btn"
                  >
                    View
                  </a>

                  <a
                    href={`http://localhost:8000${resume.file}`}
                    download
                    className="download-btn"
                  >
                    Download
                  </a>

                  <button
                    className="delete-btn"
                    onClick={() => handleDelete(resume.id)}
                  >
                    Delete
                  </button>

                </div>
              </div>

            </div>

          ))
        )}

      </div>

    </div>
    )
}
export default ResumeManager;