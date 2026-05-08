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
Title: {job_data.title}
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

    raw = response.choices[0].message.content.strip()

    # Remove markdown wrappers
    if raw.startswith("```json"):
        raw = raw.replace("```json", "").replace("```", "").strip()

    elif raw.startswith("```"):
        raw = raw.replace("```", "").strip()

    try:
        return json.loads(raw)

    except json.JSONDecodeError:
        return {
            "type": "error",
            "message": "AI returned invalid format",
            "raw": content
        }

def analyze_resume_for_questions(
    resume_text,
    job_data
):

    prompt = f"""
You are an elite ATS resume analyzer and career optimization AI.

Your task is to analyze a candidate's resume against a target job.

==================================================
TARGET JOB
==================================================

Title:
{job_data.title}

Company:
{job_data.company}

Description:
{job_data.description}

Responsibilities:
{job_data.responsibilities}

Required Skills:
{job_data.skills}

==================================================
CANDIDATE RESUME
==================================================

{resume_text}

==================================================
ANALYSIS TASK
==================================================

Carefully analyze the mismatch between:

1. The candidate's current resume
2. The target role requirements
3. Industry expectations
4. ATS keyword expectations
5. Technical stack requirements
6. Domain knowledge expectations

Detect important missing areas that should be clarified
BEFORE generating the optimized resume.

Examples:
- Fintech familiarity
- DevOps experience
- Leadership experience
- Cloud platforms
- Security experience
- Agile/Scrum usage
- Monitoring tools
- CI/CD experience
- Data engineering exposure
- AI/ML familiarity
- Startup experience
- Enterprise-scale systems
- API integrations
- Kubernetes usage
- Compliance knowledge
- Customer-facing experience

==================================================
RULES
==================================================

- Ask follow-up questions ONLY for meaningful ATS gaps
- Questions must improve ATS matching quality
- Questions must remain realistic
- NEVER fabricate experience
- NEVER exaggerate candidate background
- Questions should help improve:
    - Summary
    - Skills
    - Experience wording
    - Project descriptions
    - ATS keyword matching

- You may ask MULTIPLE questions if necessary
- Maximum questions: 5
- Each question MUST contain exactly 4 concise options
- Questions should feel professional and natural
- Avoid robotic wording
- Avoid generic AI-style buzzwords

==================================================
IMPORTANT
==================================================

If the resume already aligns well with the role,
return no questions.

==================================================
RESPONSE FORMAT
==================================================

If questions are needed:

{{
  "type": "questions",
  "questions": [
    {{
      "id": 1,
      "question": "...",
      "options": [
        "...",
        "...",
        "...",
        "..."
      ]
    }},
    {{
      "id": 2,
      "question": "...",
      "options": [
        "...",
        "...",
        "...",
        "..."
      ]
    }}
  ]
}}

If no clarification is needed:

{{
  "type": "no_questions"
}}

Return STRICT JSON ONLY.
Do not include explanations.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=300
    )

    raw = response.choices[0].message.content.strip()

    # Remove markdown wrappers
    if raw.startswith("```json"):
        raw = raw.replace("```json", "").replace("```", "").strip()

    elif raw.startswith("```"):
        raw = raw.replace("```", "").strip()

    try:
        return json.loads(raw)

    except Exception:
        return {
            "type": "no_questions"
        }