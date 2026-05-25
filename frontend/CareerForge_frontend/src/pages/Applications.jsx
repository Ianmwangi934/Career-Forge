import "./Applications.css";
import { useEffect, useState } from "react";
import axios from "axios";

import { Document, Page, pdfjs } from "react-pdf";

import workerSrc from "pdfjs-dist/build/pdf.worker?url";

pdfjs.GlobalWorkerOptions.workerSrc = workerSrc

const Applications = () =>{
    const [applications, setApplications] = useState([])

    useEffect(()=>{
        fetchApplications()
    },[])

    const fetchApplications = async () => {
        try {
            const res = await axios.get(
                "http://localhost:8000/job_applications/generated-resumes/",
                {
                    withCredentials: true
                }
            )
            setApplications(res.data)
        } catch (err) {
            console.error(err)
        }
    };

    // Delete a single Resume
    const deleteResume = async (id) => {
        const confirmDelete = window.confirm("Delete This Resume?");
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
        } catch (err) {
            console.error(err);
        }
        
    };

    // Delete all generated Resumes
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

        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="applications-page">

            <div className="applications-header">

                <h2>
                    AI Generated Resumes
                </h2>

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


            <div className="applications-grid">

                {
                    applications.map((app) => {

                        const fileUrl = app.file.startsWith("http")
                            ? app.file
                            : `http://localhost:8000${app.file}`

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
                                        className="delete-btn"
                                        onClick={() => deleteResume(app.id)}
                                    >
                                        Delete Resume
                                    </button>

                                </div>

                            </div>

                        )

                    })
                }

            </div>

        </div>

    )
}
export default Applications;