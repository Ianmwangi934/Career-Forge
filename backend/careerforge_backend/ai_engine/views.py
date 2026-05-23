from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q

from resumes.models import Resume
from job_applications.models import JobApplication, GeneratedResume
from .models import AIQuestionSession
from .models import AIQuestion
from .services.pdf_generator import generate_resume_pdf
from django.conf import settings
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from resumes.models import Resume
import json

from .utils import extract_text_from_pdf, analyze_resume_with_ai
from .grok_client import (
    generate_resume_with_groq,
    analyze_resume_for_questions
)
NEWS_API_KEY = settings.NEWS_API_KEY 



# Create your views here.

class GenerateResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            print("========== GenerateResumeView HIT ==========")
            print(request.data)

            resume_id = request.data.get("resume_id")
            job_id = request.data.get("job_id")

            print("Resume ID:", resume_id)
            print("Job ID:", job_id)

            resume = Resume.objects.get(
                id=resume_id,
                user=request.user
            )

            print("Resume fetched")

            job = JobApplication.objects.get(
                id=job_id,
                user=request.user
            )

            print("Job fetched")

            # Extract PDF text
            resume_text = extract_text_from_pdf(
                resume.file.path
            )

            print("PDF extraction successful")
            #print("Resume text length:", len(resume_text))

            # Analyze
            analysis = analyze_resume_for_questions(
                resume_text,
                job
            )

            print("Analysis complete")
            print(analysis)

            # QUESTIONS
            if analysis.get("type") == "questions":

                print("Questions detected")

                session = AIQuestionSession.objects.create(
                    user=request.user,
                    resume=resume,
                    job_application=job
                )

                #questions_data = analysis.get("questions",[])
                questions_data = analysis.get("questions")

                if not questions_data:

                    # Handle single-question format
                    questions_data = [{
                        "question": analysis.get("question"),
                        "options": analysis.get("options", [])
                    }]

                created_questions = []

                for index, q in enumerate(questions_data):

                    question = AIQuestion.objects.create(
                        session=session,
                        question=q.get("question"),
                        options=q.get("options", []),
                        order=index
                    )

                    created_questions.append({
                        "id": question.id,
                        "question": question.question,
                        "options": question.options,
                        "order": question.order
                    })

                return Response({
                    "type": "questions",
                    "session_id": session.id,
                    "questions": created_questions
                })

            print("No questions needed")

            # Generate final resume
            ai_output = generate_resume_with_groq(
                resume_text,
                job
            )

            print("Resume generation complete")
            print(ai_output)

            # AI decided more clarification is needed
            if ai_output.get("type") == "questions":

                session = AIQuestionSession.objects.create(
                    user=request.user,
                    resume=resume,
                    job_application=job
                )

                questions_data = ai_output.get("questions")

                # Handle single-question AI response
                if not questions_data:

                    questions_data = [{
                        "question": ai_output.get("question"),
                        "options": ai_output.get("options", [])
                    }]

                created_questions = []

                for index, q in enumerate(questions_data):

                    question = AIQuestion.objects.create(
                        session=session,
                        question=q.get("question"),
                        options=q.get("options", []),
                        order=index
                    )

                    created_questions.append({
                        "id": question.id,
                        "question": question.question,
                        "options": question.options,
                        "order": question.order
                    })

                return Response({
                    "type": "questions",
                    "session_id": session.id,
                    "questions": created_questions
                })

            if ai_output.get("type") == "resume":

                generated = GeneratedResume.objects.create(
                    user=request.user,
                    base_resume=resume,
                    job_application=job
                )

                resume_data = ai_output.get("content")

                pdf_url = generate_resume_pdf(
                    generated,
                    resume_data
                )

                return Response({
                    "type": "resume",
                    "message": "Resume generated",
                    "generated_id": generated.id,
                    "pdf_url": pdf_url
                })

        except Exception as e:

            import traceback

            print("========== ERROR ==========")

            traceback.print_exc()

            return Response({
                "error": str(e)
            }, status=500)

class AnswerAIQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            print("========== AnswerAIQuestionView HIT ==========")
            print(request.data)

            session_id = request.data.get("session_id")
            answers = request.data.get("answers", {})

            print("Session ID:", session_id)
            print("Answers:", answers)

            session = AIQuestionSession.objects.get(
                id=session_id,
                user=request.user
            )

            # Save all answers
            for question_id, answer in answers.items():

                print("Processing:", question_id, answer)

                try:

                    question = AIQuestion.objects.get(
                        id=question_id,
                        session=session
                    )

                    question.answer = answer
                    question.save()

                    print("Saved answer")

                except AIQuestion.DoesNotExist:

                    print("Question not found:", question_id)
                    continue

            # Check unanswered questions
            unanswered_exists = session.questions.filter(
                Q(answer__isnull=True) | Q(answer="")
            ).exists()

            print("Unanswered exists:", unanswered_exists)

            if unanswered_exists:

                return Response({
                    "message": "Answer saved",
                    "waiting_for_more_answers": True
                })

            # Mark complete
            session.completed = True
            session.save()

            # Resume/job
            resume = session.resume
            job = session.job_application

            # Extract text
            resume_text = extract_text_from_pdf(
                resume.file.path
            )

            # Build answers text
            all_answers = session.questions.all().order_by("order")

            answers_text = ""

            for q in all_answers:

                answers_text += f"""

QUESTION:
{q.question}

ANSWER:
{q.answer}

"""

            enhanced_context = f"""

The user has already answered all follow-up questions.

You MUST now generate the FINAL optimized resume.

DO NOT ask more questions.

FOLLOW-UP ANSWERS:
{answers_text}

ORIGINAL RESUME:
{resume_text}

"""

            # Generate resume
            ai_output = generate_resume_with_groq(
                enhanced_context,
                job
            )

            #print("AI OUTPUT:")
            #print(ai_output)
            if ai_output.get("type") == "questions":

                return Response({
                    "error": "AI is still asking questions",
                    "details": ai_output
                }, status=400)

            if ai_output.get("type") == "resume":

                generated = GeneratedResume.objects.create(
                    user=request.user,
                    base_resume=resume,
                    job_application=job
                )

                resume_data = ai_output.get("content")

                pdf_url = generate_resume_pdf(
                    generated,
                    resume_data
                )

                return Response({
                    "type": "resume",
                    "message": "Resume generated successfully",
                    "generated_id": generated.id,
                    "pdf_url": pdf_url
                })
            

        except Exception as e:

            import traceback

            print("========== ANSWER QUESTION ERROR ==========")
            traceback.print_exc()

            return Response({
                "error": str(e)
            }, status=500)


@api_view(["GET"])
def career_news(request):

    url = (
        "https://newsapi.org/v2/everything?"
        "q=careers OR hiring OR technology jobs OR remote work"
        "&language=en"
        "&sortBy=publishedAt"
        f"&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])
    formatted = []

    for article in articles[:10]:
        formatted.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "image": article.get("urlToImage"),
            "url": article.get("url"),
            "source": article.get("source", {}).get("name")
        })

    return Response(formatted)

@api_view(["GET"])
def resume_insights(request):

    user = request.user

    resume = Resume.objects.filter(
        user=user
    ).first()

    if not resume:

        return Response({
            "error": "No resume uploaded."
        }, status=404)

    pdf_path = resume.file.path

    resume_text = extract_text_from_pdf(
        pdf_path
    )

    data = analyze_resume_with_ai(
        resume_text
    )

    return Response(data)