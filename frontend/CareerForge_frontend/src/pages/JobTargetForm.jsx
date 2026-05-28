import "./JobTargetForm.css";
import { useState , useEffect} from "react";
import axios from "axios";
import AIQuestionCard from "./AIQuestionCard";
import { Document, Page, pdfjs } from "react-pdf";
import workerSrc from "pdfjs-dist/build/pdf.worker?url";
pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;

const JobTargetForm = () => {
    const [form, setForm] = useState({
        title:"",
        company:"",
        description:"",
        responsibilities:"",
        skills:"",
    })
    const [aiQuestions, setAiQuestions] = useState(null)
    const [generatedResume, setGeneratedResume] = useState(null)
    const [resumes, setResumes] = useState([]);
    const [showSuccessAlert, setShowSuccessAlert] = useState(false)
    const [resumeImprovements, setResumeImprovements] = useState([])

    const [loading, setLoading] = useState(false)
    // You must have a resume selected
        useEffect(() => {
            const fetchResumes = async () => {
                try {
                    const res = await axios.get(
                        "http://localhost:8000/resumes/",
                        { withCredentials: true }
                    );

                    setResumes(res.data);
                } catch (err) {
                    console.error("Failed to fetch resumes", err);
                }
            };

            fetchResumes();
        }, []);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]:e.target.value
        })
    }

    const handleSubmit = async (e) => {
    e.preventDefault()

    const hasInput = Object.values(form).some(
        val => val.trim() !== ""
    )

    if (!hasInput) {
        alert("Please fill at least one field.")
        return
    }

    try {

        setLoading(true)

        // STEP 1:
        // Save Job Application
        const jobRes = await axios.post(
            "http://localhost:8000/job_applications/",
            form,
            {
                withCredentials: true
            }
        )

        const jobId = jobRes.data.id

        // IMPORTANT:
        

        // STEP 2:
        // Trigger AI analysis
        if (resumes.length === 0) {
            alert("Please upload a resume first.")
            return
        }
        const aiRes = await axios.post(
            "http://localhost:8000/ai_engine/generate/",
            {
                //resume_id: resumeId,
                resume_id: resumes[0]?.id,
                job_id: jobId
            },
            {
                withCredentials: true
            }
        )

        // QUESTIONS
        if (aiRes.data.type === "questions") {

            setAiQuestions({
                sessionId: aiRes.data.session_id,
                questions: aiRes.data.questions
            })

        }

        // DIRECT RESUME
        else if (
            aiRes.data.type === "resume"
        ) {

            setGeneratedResume(aiRes.data)

            setResumeImprovements(
                aiRes.data.improvements || []
            )

            setShowSuccessAlert(true)

        }

        // RESET
        setForm({
            title:"",
            company:"",
            description:"",
            responsibilities:"",
            skills:"",
        })

    } catch (err) {

        console.error(err)

        alert("Something went wrong.")

    } finally {

        setLoading(false)

    }
}

    return (
        <div className="job-form-container">

            <h2>Target a Job with AI</h2>
            <p className="subtitle">
                Provide details about the job you’re applying for. 
                The more you add, the smarter your resume will be.
            </p>

            <form onSubmit={handleSubmit} className="job-form">

                <input
                type="text"
                name="title"
                placeholder="Job Title (e.g. Backend Developer)"
                value={form.title}
                onChange={handleChange}
                />
                <input
                type="text"
                name="company"
                placeholder="Company (optional)"
                value={form.company}
                onChange={handleChange}
                />

                <textarea
                name="description"
                placeholder="Job Description"
                value={form.description}
                onChange={handleChange}
                />

                <textarea
                name="responsibilities"
                placeholder="Responsibilities"
                value={form.responsibilities}
                onChange={handleChange}
                />

                <textarea
                name="skills"
                placeholder="Required Skills"
                value={form.skills}
                onChange={handleChange}
                />

                <button type="submit" disabled={loading}>
                {loading ? "Analyzing your Resume with the Job Description..." : "Save & We analyze your Resume for the Job"}
                </button>

            </form>

            
            {
            aiQuestions && (
                <AIQuestionCard
                sessionId={aiQuestions.sessionId}
                questions={aiQuestions.questions}

                onComplete={(data) => {

                    setAiQuestions(null)

                    setGeneratedResume(data)
                    setResumeImprovements(
                        data.improvements || []
                    )

                    setShowSuccessAlert(true)
                }}
                />
            )
            }

            {
                showSuccessAlert && (

                    <div className="custom-alert-overlay">

                        <div className="custom-alert">

                            <div className="success-icon">
                                🚀
                            </div>

                            <h2>
                                Resume Optimized Successfully
                            </h2>

                            <p className="alert-subtext">
                                AI improved your resume for this role.
                            </p>

                            {
                                resumeImprovements.length > 0 && (

                                    <div className="improvement-section">

                                        <h3>
                                            Improvements Made
                                        </h3>

                                        <ul className="improvement-list">

                                            {
                                                resumeImprovements.map((item, index) => (

                                                    <li key={index} className="improvement-item">

                                                        <div className="improvement-title">
                                                            ✨ {item.title}
                                                        </div>

                                                        <div className="improvement-description">
                                                            {item.description}
                                                        </div>

                                                    </li>

                                                ))
                                            }

                                        </ul>

                                    </div>

                                )
                            }

                            <button
                                onClick={() =>
                                    setShowSuccessAlert(false)
                                }
                                className="alert-btn"
                            >
                                View Resume
                            </button>

                        </div>

                    </div>

                )
            }

            {
                generatedResume && (

                    <div className="resume-modal-overlay">

                        <div className="generated-resume-box">

                            <button
                                className="close-modal-btn"
                                onClick={() => setGeneratedResume(null)}
                            >
                                ×
                            </button>

                            <h2>
                                Your AI Optimized Resume
                            </h2>

                            <div className="generated-actions">

                                <a
                                    href={`http://localhost:8000${generatedResume.pdf_url}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="view-btn"
                                >
                                    View Resume
                                </a>

                                <a
                                    href={`http://localhost:8000${generatedResume.pdf_url}`}
                                    download
                                    className="download-btn"
                                >
                                    Download PDF
                                </a>

                            </div>

                            <div className="generated-preview">

                                <Document
                                    file={`http://localhost:8000${generatedResume.pdf_url}`}
                                    onLoadError={(err) =>
                                        console.error(
                                            "PDF Preview Error:",
                                            err
                                        )
                                    }
                                >

                                    <Page
                                        pageNumber={1}
                                        width={420}
                                    />

                                </Document>

                            </div>

                        </div>

                    </div>

                )
            }

    </div>
    )
}
export default JobTargetForm;