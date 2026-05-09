import "./JobTargetForm.css";
import { useState , useEffect} from "react";
import axios from "axios";
import AIQuestionCard from "./AIQuestionCard";

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

            alert("Resume generated 🚀")

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
                {loading ? "Saving..." : "Save & We analyze your Resume for the Job"}
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

                    alert("AI Resume Generated Successfully 🚀")
                }}
                />
            )
            }

    </div>
    )
}
export default JobTargetForm;