import fitz
from django.conf import settings
from groq import Groq
import json
import re
client = Groq(api_key=settings.GROQ_API_KEY)

def extract_text_from_pdf(file_path):
    text = ""

    with fitz.open(file_path) as doc:
        for page in doc:
            text +=page.get_text()

    return text

def analyze_resume_with_ai(resume_text):

    prompt = f"""
    You are a professional resume reviewer and ATS analyst.

Your task is to carefully analyze the ENTIRE resume provided below.

IMPORTANT RULES:

1. Read EVERY section of the resume from beginning to end.
2. Read every word, sentence, bullet point, project description, certification, technology stack, skill list, education section, and work experience section.
3. Before generating your response, build an internal list of ALL skills, technologies, tools, programming languages, frameworks, cloud platforms, databases, methodologies, and certifications explicitly mentioned anywhere in the resume.
4. NEVER classify a skill as missing if it appears anywhere in the resume.
5. A skill is considered "missing" ONLY if:

   * It does NOT appear anywhere in the resume.
   * It is highly relevant to the candidate's target career path based on their existing skills and experience.
6. Do not infer that a skill is missing simply because it is not emphasized enough.
7. Do not recommend a skill that already exists in the resume.
8. Strengths must be supported by evidence found directly in the resume.
9. Recommendations must be actionable and based on actual gaps or improvement opportunities.
10. Market trends should focus on skills and technologies currently in demand that are NOT already present in the resume.





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
        temperature=0.2,
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
        temperature=0.1
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

    # Extract the first JSON object from the response
    match = re.search(r"\{.*\}", content, re.DOTALL)

    if match:
        content = match.group(0)

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        print("Invalid JSON returned by model:")
        print(content)

        return {
            "difficulty": "Unknown",
            "focus_areas": [],
            "likely_questions": [],
            "behavioral_questions": [],
            "weak_areas": [],
            "tips": [
                "AI failed to generate interview preparation."
            ]
        }

    #print("========== CLEANED CONTENT ==========")
    #print(content)

    try:
        return json.loads(content)

    except json.JSONDecodeError:

        print("Invalid JSON returned by model:")
        print(content)

        return {
            "difficulty": "Unknown",
            "focus_areas": [],
            "likely_questions": [],
            "behavioral_questions": [],
            "weak_areas": [],
            "tips": [
                "AI failed to generate interview preparation."
            ]
        }


def generate_first_interview_question(resume_text,job):
    prompt = f"""
    You are an expert interviewer.

    You are interviewing a candidate for:

    TITLE:
    {job.title}

    COMPANY:
    {job.company}

    DESCRIPTION:
    {job.description}

    RESPONSIBILITIES:
    {job.responsibilities}

    SKILLS:
    {job.skills}

    TAILORED RESUME:
    {resume_text}

    TASK:

    Generate the BEST first interview question.

    The question should be based on:

    - candidate resume
    - target role
    - candidate projects
    - candidate experience

    Do NOT ask generic questions.

    Return JSON only:

    {{
        "question": "",
        "category": ""
    }}

    Possible categories:

    technical
    behavioral
    system_design
    project_deep_dive
    problem_solving
    leadership
    communication
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

    content = response.choices[0].message.content.strip()

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


def evaluate_interview_answer(
    question,
    category,
    answer,
    resume_text,
    job
):
    prompt = f"""
You are a brutally honest senior interviewer.

JOB TITLE:
{job.title}

COMPANY:
{job.company}

DESCRIPTION:
{job.description}

SKILLS:
{job.skills}

RESUME:
{resume_text}

QUESTION:
{question}

CATEGORY:
{category}

CANDIDATE ANSWER:
{answer}

TASK:

1. Score the answer.
2. Critique it honestly.
3. Evaluate:
   - technical accuracy
   - communication
   - confidence
4. Provide an ideal answer.
5. Generate the next interview question.

Return JSON only:

{{
    "score": 0,
    "technical_score": 0,
    "communication_score": 0,
    "confidence_score": 0,
    "feedback": "",
    "ideal_answer": "",
    "next_question": "",
    "next_category": ""
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
        temperature=0.4
    )

    content = response.choices[0].message.content.strip()

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
