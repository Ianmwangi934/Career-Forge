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
    }

    return (
        <div className="applications-page">

            <h2>
                AI Generated Resumes
            </h2>

            <div className="applications-grid">

                {
                    applications.map((app) => {

                        const fileUrl =
                            `http://localhost:8000${app.file}`

                        return (

                            <div
                                key={app.id}
                                className="application-card"
                            >

                                <a
                                    href={fileUrl}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >

                                    <Document file={fileUrl}>

                                        <Page
                                            pageNumber={1}
                                            width={220}
                                        />

                                    </Document>

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