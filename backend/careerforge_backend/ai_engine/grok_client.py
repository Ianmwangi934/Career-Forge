from django.conf import settings
from groq import Groq
import json 


client = Groq(api_key=settings.GROQ_API_KEY)

def generate_resume_with_groq(resume_text, job_data):
    prompt = f"""
    You are a professional resume optimizer and ATS expert.

=====================
JOB DETAILS
=====================
Title: {job_data.job_title}
Company: {job_data.company}
Description: {job_data.description}
Responsibilities: {job_data.responsibilities}
Skills: {job_data.skills}

=====================
ORIGINAL RESUME
=====================
{resume_text}

=====================
STRICT INSTRUCTIONS
=====================

1. Preserve the ORIGINAL STRUCTURE and FORMAT of the resume:
   - Keep section order (Summary, Skills, Experience, Projects, etc.)
   - Do NOT redesign the resume
   - Only improve content inside sections

2. Optimize for ATS (Applicant Tracking Systems):
   - Include relevant keywords from job description
   - Match terminology used in the job posting
   - Ensure readability by ATS parsers

3. Avoid AI-like writing:
   - Do NOT use generic buzzwords (e.g. "results-driven", "dynamic professional")
   - Use natural, human-like, concise language

4. DO NOT fabricate experience:
   - Only enhance what exists
   - Keep everything realistic

5. Industry alignment:
   - Adapt wording to match the company's industry

6. Improve:
   - Summary
   - Skills
   - Experience

7. If critical domain experience is missing:
Return:
{{
  "type": "question",
  "question": "Do you have experience in [domain]?",
  "options": ["Yes", "No", "Familiar", "Willing to learn"]
}}

8. Otherwise return:
{{
  "type": "resume",
  "content": "FULL OPTIMIZED RESUME TEXT HERE"
}}

=====================
IMPORTANT
=====================
- Output MUST be valid JSON
- No explanations
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=2000,
    )

    content = response.choices[0].message.content.strip()

    #  Critical: safely parse JSON
    try:
        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "type": "error",
            "message": "AI returned invalid format",
            "raw": content
        }