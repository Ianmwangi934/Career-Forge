import fitz
from django.conf import settings
from groq import Groq
import json
client = Groq(api_key=settings.GROQ_API_KEY)

def extract_text_from_pdf(file_path):
    text = ""

    with fitz.open(file_path) as doc:
        for page in doc:
            text +=page.get_text()

    return text

def analyze_resume_with_ai(resume_text):

    prompt = f"""
    Analyze this resume professionally.

    Resume:
    {resume_text}

    Return JSON only in this format:

    {{
      "strengths": [],
      "missing_skills": [],
      "recommendations": [],
      "market_trends": []
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content.strip()

    print(content)

    # Remove markdown
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()

    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    return json.loads(content)


def generate_resume_improvements(
    original_resume,
    optimized_resume,
    job_data
):

    prompt = f"""
You are an elite ATS resume reviewer.

Your task is to compare:

1. ORIGINAL RESUME
2. OPTIMIZED RESUME
3. TARGET JOB

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

Skills:
{job_data.skills}

==================================================
ORIGINAL RESUME
==================================================

{original_resume}

==================================================
OPTIMIZED RESUME
==================================================

{optimized_resume}

==================================================
TASK
==================================================

Analyze the improvements made to the resume.

Focus on:
- ATS optimization
- Keyword matching
- Technical alignment
- Business impact
- Clarity improvements
- Professional language
- Resume personalization
- Industry terminology
- Metrics/value improvements
- Stronger project descriptions
- Better skill alignment

==================================================
IMPORTANT RULES
==================================================

- Be concise
- Be specific
- Be realistic
- Do NOT exaggerate
- Do NOT mention fake improvements
- Maximum 8 improvements
- Each point should feel meaningful
- Each point should help user understand WHY the resume improved

==================================================
RETURN FORMAT
==================================================

Return STRICT JSON ONLY:

{{
  "improvements": [
    {{
      "title": "ATS Keywords Improved",
      "description": "Added relevant technical keywords matching the target role requirements."
    }},
    {{
      "title": "Project Impact Strengthened",
      "description": "Improved project descriptions with clearer business value and measurable impact."
    }}
  ]
}}

Return ONLY valid JSON.
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
        max_tokens=600
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
            "improvements": [
                {
                    "title": "Resume Optimized",
                    "description": "Your resume was tailored to better match the target role."
                }
            ]
        }

#Generating application emails for users
def generate_application_email(
    resume_text,
    job_data
):

    prompt = f"""
You are an experienced recruiter and hiring manager.

Generate a REALISTIC job application email that a candidate would actually send.

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

Skills:
{job_data.skills}

==================================================
CANDIDATE RESUME
==================================================

{resume_text}

==================================================
GOAL
==================================================

Create a short job application email that feels:

- Human
- Natural
- Friendly
- Professional
- Genuine

The email should NOT sound like AI.

The email should NOT sound like a cover letter.

The email should NOT use overly formal language.

==================================================
EMAIL GUIDELINES
==================================================

The email should:

- Mention the position being applied for
- Briefly reference relevant experience or skills
- Show genuine interest in the opportunity
- Mention that the resume is attached
- Thank the recruiter for their time

The email should read like something a real applicant
would type before attaching their resume.

==================================================
AVOID
==================================================

Do NOT use phrases like:

- "I am writing to express my interest..."
- "Please find attached..."
- "To whom it may concern..."
- "I believe I would be a valuable asset..."
- "I am excited to submit my application..."
- Generic corporate language
- Buzzword-heavy wording

==================================================
STYLE
==================================================

- Conversational
- Professional
- Authentic
- Confident but not arrogant
- Under 150 words

==================================================
RETURN JSON ONLY
==================================================

{{
    "subject": "",
    "email_body": ""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    content = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    if content.startswith("```json"):
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    elif content.startswith("```"):
        content = (
            content
            .replace("```", "")
            .strip()
        )

    return json.loads(content)


def generate_interview_prep(resume_text,job):


    prompt = f"""
You are an expert technical recruiter and interview coach.

Analyze:

RESUME:
{resume_text}

JOB TITLE:
{job.title}

COMPANY:
{job.company}

DESCRIPTION:
{job.description}

RESPONSIBILITIES:
{job.responsibilities}

SKILLS:
{job.skills}

Generate interview preparation advice.

Return JSON only:

{{
    "difficulty": "",
    "focus_areas": [],
    "likely_questions": [],
    "behavioral_questions": [],
    "weak_areas": [],
    "tips": []
}}

Rules:

- Questions must be specific to this job
- Questions must reflect the candidate's resume
- Questions must reflect missing skills
- Do not generate generic interview advice
- Do not generate answers
- Keep questions realistic
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    content = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    print("========== INTERVIEW PREP RAW ==========")
    print(content)

    if content.startswith("```json"):
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    elif content.startswith("```"):
        content = (
            content
            .replace("```", "")
            .strip()
        )

    print("========== CLEANED CONTENT ==========")
    print(content)

    return json.loads(content)