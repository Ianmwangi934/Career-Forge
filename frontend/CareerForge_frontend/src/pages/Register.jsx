import "./Auth.css"
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Register = () => {
    const navigate = useNavigate()

    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const handleSubmit = async(e) => {
        e.preventDefault()

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/accounts/register/",
                {
                    username,
                    email,
                    password
                },
                {
                    withCredentials:true  // We are using HttpOnlyCookies
                }
            )
            //console.log(response.data)
            // Redirect after success
            navigate("/")
        }

        catch (error) {
            console.error(error.response?.data || error.message)
        }
    }

    return (
        <div className="auth-container">
      <div className="auth-card">

        <h1 className="auth-title">Create Account</h1>
        <p className="auth-subtitle">
          Start shaping your career today
        </p>

        <form onSubmit={handleSubmit} className="auth-form">

          <div className="input-group">
            <label>Username</label>
            <input
              type="text"
              placeholder="yourname"
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" className="auth-btn">
            Register
          </button>

        </form>

        <p className="auth-switch">
          Already have an account?{" "}
          <span onClick={() => navigate("/login")}>Login</span>
        </p>

      </div>
    </div>
    )
}
export default Register;