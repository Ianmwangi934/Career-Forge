import "./Home.css"
import { useNavigate } from "react-router-dom"

import heroImage from "../assets/careerforge-hero.png"

const Home = () => {

    const navigate = useNavigate()

    return (
        <div className="home-container">
            <h1 className="head">CareerForge ✨</h1>

            <div className="home-wrapper">

                {/* LEFT SIDE */}
                <div className="home-card">

                    <h1 className="logo">
                        CareerForge
                    </h1>

                    <p className="tagline">
                        Shaping your career intentionally.
                    </p>

                    <p className="subtitle">
                        AI-powered resume tailoring,
                        cover letters, and interview prep —
                        all in one place.
                    </p>

                    <div className="buttons">

                        <button
                            onClick={() => navigate("/login")}
                            className="btn primary"
                        >
                            Login
                        </button>

                        <button
                            onClick={() => navigate("/register")}
                            className="btn secondary"
                        >
                            Register
                        </button>

                    </div>

                </div>

                {/* RIGHT SIDE */}
                <div className="home-image-container">

                    <img
                        src={heroImage}
                        alt="CareerForge Hero"
                        className="home-image"
                    />

                </div>

            </div>

        </div>
    )
}

export default Home