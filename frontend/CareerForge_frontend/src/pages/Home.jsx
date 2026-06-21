import "./Home.css";
import { useNavigate } from "react-router-dom";

import heroImage from "../assets/Career.png";

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="home-container">

            <div className="home-wrapper">

                {/* LEFT SIDE */}
                <div className="home-content">

                    <h1 className="logo">
                        CareerForge
                    </h1>

                    <h2 className="hero-title">
                        Build stronger applications with AI.
                    </h2>

                    <p className="hero-description">
                        CareerForge helps professionals tailor resumes,
                        prepare for interviews, generate application materials,
                        and organize their job search from a single platform.
                    </p>

                    <div className="feature-list">

                        <div className="feature-item">
                            Resume Tailoring
                        </div>

                        <div className="feature-item">
                            Interview Preparation
                        </div>

                        <div className="feature-item">
                            Application Tracking
                        </div>

                    </div>

                    <div className="buttons">

                        <button
                            onClick={() => navigate("/register")}
                            className="btn primary"
                        >
                            Get Started
                        </button>

                        <button
                            onClick={() => navigate("/login")}
                            className="btn secondary"
                        >
                            Sign In
                        </button>

                    </div>

                </div>

                {/* RIGHT SIDE */}

                <div className="home-image-container">

                    <img
                        src={heroImage}
                        alt="CareerForge Dashboard"
                        className="home-image"
                    />

                </div>

            </div>

        </div>
    );
};

export default Home;