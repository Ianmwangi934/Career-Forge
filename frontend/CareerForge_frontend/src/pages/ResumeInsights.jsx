import "./ResumeInsights.css"
import { useEffect, useState } from "react";
import axios from "axios";
import Strength from "../assets/Strength.jpeg"
import Recomendations from "../assets/Recomendations.jpeg"
import Missing from "../assets/missing.jpeg"
import Market from "../assets/market.jpeg"

const ResumeInsights = () => {
    const [insights, setInsights] = useState(null)

    const [loading, setLoading] = useState(true)


    useEffect(()=>{
        const fetchInsights = async () =>{
            try {
                const res = await axios.get(
                    "http://80.225.78.96/ai_engine/resume-insights/",

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
                        src={Strength}
                        alt="Strengths"
                    />
                                        

                    <div className="insight-content">

                        <h3>
                            Strengths
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
                        src={Missing}
                        alt="Missing Skills"
                    />

                    <div className="insight-content">

                        <h3>
                             Missing Skills
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
                        src={Market}
                        alt="Market Trends"
                    />

                    <div className="insight-content">

                        <h3>
                             Market Trends
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
                        src={Recomendations}
                        alt="Recommendations"
                    />

                    <div className="insight-content">

                        <h3>
                             Recommendations
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