import "./Auth.css"
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios";

const Login = () => {
    const navigate = useNavigate()

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const handleSubmit = async(e) => {
        e.preventDefault()

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/accounts/login/",
                {
                    email,
                    password
                },
                {
                    withCredentials:true
                }
            )
            console.log(response.data)
            navigate("/")

        } catch (error) {
            console.error(error.response?.data || error.message)
        }
    }

    return (
        <div className="auth-container">
      <div className="auth-card">

        <h1 className="auth-title">Welcome Back</h1>
        <p className="auth-subtitle">
          Login to continue building your career intentionally
        </p>

        <form onSubmit={handleSubmit} className="auth-form">

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
            Login
          </button>

        </form>

        <p className="auth-switch">
          Don’t have an account?{" "}
          <span onClick={() => navigate("/register")}>Register</span>
        </p>

      </div>
    </div>
    )
}
export default Login;