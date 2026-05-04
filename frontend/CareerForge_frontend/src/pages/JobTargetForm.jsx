import "./JobTargetForm.css";
import { useState } from "react";
import axios from "axios";

const JobTargetForm = () => {
    const [form, setForm] = useState({
        title:"",
        company:"",
        description:"",
        responsibilities:"",
        skills:"",
    })

    const [loading, setLoading] = useState(false)

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]:e.target.value
        })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        // Validation: At least one field
        const hasInput = Object.values(form).some(val => val.trim() !=="")
        if (!hasInput) {
            alert("Please fill at least one field.")
            return
        }

        try {
            setLoading(true)

            await axios.post(
                "http://localhost:8000/job_applications/",
                form,
                {withCredentials:true}
            )
            // Reset form
            setForm({
                title:"",
                company:"",
                description:"",
                responsibilities:"",
                skills:""
            })

            // Future AI hook
            alert("Job data saved. AI resume generation coming soon 🚀")

        } catch (err) {
            console.error("Submission failed:", err)
            alert("Something went wrong. Try again.")
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
                name="job_title"
                placeholder="Job Title (e.g. Backend Developer)"
                value={form.job_title}
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
                {loading ? "Saving..." : "Save & Generate Resume"}
                </button>

            </form>

    </div>
    )
}
export default JobTargetForm;