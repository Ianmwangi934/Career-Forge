import "./ResumeInsights.css"
import { useEffect, useState } from "react";
import axios from "axios";

const ResumeInsights = () => {
    const [insights, setInsights] = useState(null)

    const [loading, setLoading] = useState(true)


    useEffect(()=>{
        const fetchInsights = async () =>{
            try {
                const res = await axios.get(
                    "http://localhost:8000/ai_engine/resume-insights/",

                    {
                        withCredentials: true
                    }
                )
                setInsights(res.data)
            } catch (err) {
                console.error(err)

            } finally {
                setLoading(false)

            }
        }

        fetchInsights()
    },[])

    if (loading) {
        return (
            <div className="insights-loading">
                AI is analyzing your resume...
            </div>
        )
    }

    if (!insights) {
        return null
    }


    return (
        <div className="resume-insights">

            <h2 className="insights-title">
                AI Resume Intelligence
            </h2>

            <div className="insights-grid">

                {/* STRENGTHS */}
                <div className="insight-card strengths">

                    <img
                        src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f"
                        alt="Strengths"
                    />

                    <div className="insight-content">

                        <h3>
                            ✅ Strengths
                        </h3>

                        <ul>

                            {
                                insights.strengths?.map(
                                    (item, index) => (
                                        <li key={index}>
                                            {item}
                                        </li>
                                    )
                                )
                            }

                        </ul>

                    </div>

                </div>

                {/* MISSING SKILLS */}
                <div className="insight-card missing">

                    <img
                        src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3"
                        alt="Missing Skills"
                    />

                    <div className="insight-content">

                        <h3>
                            ⚠ Missing Skills
                        </h3>

                        <ul>

                            {
                                insights.missing_skills?.map(
                                    (item, index) => (
                                        <li key={index}>
                                            {item}
                                        </li>
                                    )
                                )
                            }

                        </ul>

                    </div>

                </div>

                {/* MARKET TRENDS */}
                <div className="insight-card trends">

                    <img
                        src="https://images.unsplash.com/photo-1460925895917-afdab827c52f"
                        alt="Market Trends"
                    />

                    <div className="insight-content">

                        <h3>
                            📈 Market Trends
                        </h3>

                        <ul>

                            {
                                insights.market_trends?.map(
                                    (item, index) => (
                                        <li key={index}>
                                            {item}
                                        </li>
                                    )
                                )
                            }

                        </ul>

                    </div>

                </div>

                {/* RECOMMENDATIONS */}
                <div className="insight-card recommendations">

                    <img
                        src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40"
                        alt="Recommendations"
                    />

                    <div className="insight-content">

                        <h3>
                            🧠 Recommendations
                        </h3>

                        <ul>

                            {
                                insights.recommendations?.map(
                                    (item, index) => (
                                        <li key={index}>
                                            {item}
                                        </li>
                                    )
                                )
                            }

                        </ul>

                    </div>

                </div>

            </div>

        </div>

    )
}
export default ResumeInsights