import "./Applications.css";
import { useEffect, useState } from "react";
import axios from "axios";

import { Document, Page, pdfjs } from "react-pdf";

import workerSrc from "pdfjs-dist/build/pdf.worker?url";

pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;

const Applications = () => {

    const [applications, setApplications] = useState([]);
    const [analytics, setAnalytics] = useState(null);

    useEffect(() => {

        fetchApplications();
        fetchAnalytics();

    }, []);

    // FETCH RESUMES
    const fetchApplications = async () => {

        try {

            const res = await axios.get(
                "http://localhost:8000/job_applications/generated-resumes/",
                {
                    withCredentials: true
                }
            );

            setApplications(res.data);

        } catch (err) {

            console.error(err);

        }
    };

    // FETCH ANALYTICS
    const fetchAnalytics = async () => {

        try {

            const res = await axios.get(
                "http://localhost:8000/ai_engine/resume-analytics/",
                {
                    withCredentials: true
                }
            );

            setAnalytics(res.data);

        } catch (err) {

            console.error(err);

        }
    };

    // DELETE SINGLE
    const deleteResume = async (id) => {

        const confirmDelete = window.confirm(
            "Delete this generated resume?"
        );

        if (!confirmDelete) return;

        try {

            await axios.delete(
                `http://localhost:8000/ai_engine/generated-resumes/${id}/delete/`,
                {
                    withCredentials: true
                }
            );

            setApplications(
                applications.filter(
                    (app) => app.id !== id
                )
            );

            fetchAnalytics();

        } catch (err) {

            console.error(err);

        }
    };

    // DELETE ALL
    const deleteAllResumes = async () => {

        const confirmDelete = window.confirm(
            "Delete ALL generated resumes?"
        );

        if (!confirmDelete) return;

        try {

            await axios.delete(
                "http://localhost:8000/ai_engine/generated-resumes/delete-all/",
                {
                    withCredentials: true
                }
            );

            setApplications([]);
            fetchAnalytics();

        } catch (err) {

            console.error(err);

        }
    };

    return (

        <div className="applications-page">

            {/* HEADER */}
            <div className="applications-header">

                <div>

                    <h2>
                        AI Generated Resumes
                    </h2>

                    <p className="applications-subtitle">
                        Tailored resumes optimized for specific opportunities.
                    </p>

                </div>

                {
                    applications.length > 0 && (

                        <button
                            className="delete-all-btn"
                            onClick={deleteAllResumes}
                        >
                            Delete All
                        </button>

                    )
                }

            </div>

            {/* ANALYTICS */}
            {
                analytics && (

                    <div className="analytics-section">

                        <div className="analytics-card">
                           <div className="analytics-icon">
                             📄
                            </div>
                            <h3>Total Generated</h3>
                            <p>{analytics.total_generated}</p>
                        </div>

                        <div className="analytics-card">
                            <div className="analytics-icon">
                                🎯
                             </div>
                            <h3>Most Targeted Role</h3>
                            <p>{analytics.most_targeted_role}</p>
                        </div>

                        <div className="analytics-card">
                            <div className="analytics-icon">
                              🏢
                             </div>
                            <h3>Most Targeted Company</h3>
                            <p>{analytics.most_targeted_company}</p>
                        </div>

                        <div className="analytics-card">
                            <div className="analytics-icon">
                                📈
                            </div>
                            <h3>This Month</h3>
                            <p>{analytics.monthly_generation_count}</p>
                        </div>

                        <div className="analytics-card">
                            <div className="analytics-icon">
                                🚀
                            </div>
                            <h3>Career Momentum</h3>
                            <p>{analytics.career_momentum}</p>
                        </div>

                        <div className="analytics-card">
                            <div className="analytics-icon">
                                ⚡
                            </div>
                            <h3>Tailored Resumes</h3>
                            <p>
                                {analytics.tailored_resume_percentage}%
                            </p>
                        </div>

                    </div>

                )
            }

            {/* RESUME GRID */}
            <div className="applications-grid">

                {
                    applications.map((app) => {

                        const fileUrl = app.file.startsWith("http")
                            ? app.file
                            : `http://localhost:8000${app.file}`;

                        return (

                            <div
                                key={app.id}
                                className="application-card"
                            >

                                <a
                                    href={fileUrl}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="application-link"
                                >

                                    <div className="application-preview">

                                        <Document file={fileUrl}>

                                            <Page
                                                pageNumber={1}
                                                width={150}
                                            />

                                        </Document>

                                    </div>

                                </a>

                                <div className="application-info">

                                    <h3>
                                        {app.job_title}
                                    </h3>

                                    <p>
                                        {app.company}
                                    </p>

                                    <span>
                                        {
                                            new Date(
                                                app.created_at
                                            ).toLocaleDateString()
                                        }
                                    </span>

                                    <button
                                        className="application-delete-btn"
                                        onClick={() => deleteResume(app.id)}
                                    >
                                        Delete Resume
                                    </button>

                                </div>

                            </div>

                        );

                    })
                }

            </div>

        </div>

    );
};

export default Applications;