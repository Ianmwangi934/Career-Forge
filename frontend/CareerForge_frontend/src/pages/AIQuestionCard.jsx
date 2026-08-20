import "./AIQuestionCard.css";
import { useState } from "react";
import axios from "axios";

const AIQuestionCard = ({
  sessionId,
  questions,
  onComplete
}) => {

  const [answers, setAnswers] = useState({})
  const [loading, setLoading] = useState(false)

  const handleSelect = (questionId, option) => {
    setAnswers({
      ...answers,
      [questionId]: option
    })
  }

  const handleSubmit = async () => {

    // Validate all answered
    if (Object.keys(answers).length !== questions.length) {
      alert("Please answer all questions.")
      return
    }

    try { 

      setLoading(true)

      const res = await axios.post(
        "/ai_engine/answer-question/",
        {
          session_id: sessionId,
          answers: answers
        },
        {
          withCredentials: true
        }
      )

      onComplete(res.data)

    } catch (err) {

      console.error("AI answer failed:", err)
      alert("Something went wrong")

    } finally {

      setLoading(false)

    }
  }

  return (
    <div className="ai-question-overlay">

      <div className="ai-question-card">

        <div className="ai-badge">
          AI Follow-Up
        </div>

        <h2>
          Help us personalize your resume
        </h2>

        {
          questions.map((q) => (

            <div
              key={q.id}
              className="question-block"
            >

              <p className="ai-question">
                {q.question}
              </p>

              <div className="options-list">

                {
                  q.options.map((option, index) => (

                    <label
                      key={index}
                      className={`option-item ${
                        answers[q.id] === option
                          ? "selected"
                          : ""
                      }`}
                    >

                      <input
                        type="radio"
                        name={`question-${q.id}`}
                        value={option}
                        checked={answers[q.id] === option}
                        onChange={() =>
                          handleSelect(q.id, option)
                        }
                      />

                      <span>{option}</span>

                    </label>

                  ))
                }

              </div>

            </div>

          ))
        }

        <button
          className="submit-answer-btn"
          onClick={handleSubmit}
          disabled={loading}
        >
          {
            loading
              ? "Generating Resume..."
              : "Continue with AI"
          }
        </button>

      </div>

    </div>
  )
}

export default AIQuestionCard;
