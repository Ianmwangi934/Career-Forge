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