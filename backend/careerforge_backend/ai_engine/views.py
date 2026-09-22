from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q, Count
from collections import Counter
from django.utils import timezone
from datetime import timedelta

from resumes.models import Resume
from job_applications.models import JobApplication, GeneratedResume
from .models import AIQuestionSession, MockInterviewSession, MockInterviewMessage
from .models import AIQuestion
from .services.pdf_generator import generate_resume_pdf
from django.conf import settings
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from resumes.models import Resume
import json

from .utils import extract_text_from_pdf,extract_links_from_pdf, analyze_resume_with_ai, generate_resume_improvements, generate_application_email, generate_interview_prep, generate_first_interview_question, evaluate_interview_answer
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

            # Extract original clickable links
            original_links = extract_links_from_pdf(
                resume.file.path
            )

            print("PDF extraction successful")
            print("Original PDF links:", original_links)

            # Analyze
            analysis = analyze_resume_for_questions(
                resume_text,
                job
            )

            print("Analysis complete")
            # print(analysis)

            # QUESTIONS
            if analysis.get("type") == "questions":

                print("Questions detected")

                session = AIQuestionSession.objects.create(
                    user=request.user,
                    resume=resume,
                    job_application=job
                )

                # questions_data = analysis.get("questions", [])
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
                job,
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

                # Preserve original clickable links
                if original_links.get("linkedin"):
                    resume_data["linkedin"] = original_links["linkedin"]

                if original_links.get("github"):
                    resume_data["github"] = original_links["github"]

                if original_links.get("portfolio"):
                    resume_data["portfolio"] = original_links["portfolio"]

                # Resume Improvements Summary
                improvements = generate_resume_improvements(
                    resume_text,
                    json.dumps(resume_data),
                    job
                )

                pdf_url = generate_resume_pdf(
                    generated,
                    resume_data
                )

                return Response({
                    "type": "resume",
                    "message": "Resume generated",
                    "generated_id": generated.id,
                    "job_id": job.id,
                    "pdf_url": pdf_url,
                    "improvements": improvements.get(
                        "improvements",
                        []
                    )
                })

            # Fallback safety response
            return Response({
                "error": "Unexpected AI response",
                "details": ai_output
            }, status=400)

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

            # -------------------------------------------------
            # Save all answers
            # -------------------------------------------------

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

            # -------------------------------------------------
            # Check unanswered questions
            # -------------------------------------------------

            unanswered_exists = session.questions.filter(
                Q(answer__isnull=True) | Q(answer="")
            ).exists()

            print("Unanswered exists:", unanswered_exists)

            if unanswered_exists:

                return Response({
                    "message": "Answer saved",
                    "waiting_for_more_answers": True
                })

            # -------------------------------------------------
            # Mark session complete
            # -------------------------------------------------

            session.completed = True
            session.save()

            # -------------------------------------------------
            # Get original resume and job
            # -------------------------------------------------

            resume = session.resume
            job = session.job_application

            # -------------------------------------------------
            # Extract original resume text
            # -------------------------------------------------

            resume_text = extract_text_from_pdf(
                resume.file.path
            )

            # -------------------------------------------------
            # Extract original clickable links
            # -------------------------------------------------

            original_links = extract_links_from_pdf(
                resume.file.path
            )

            print("========== ORIGINAL PDF LINKS ==========")
            print("LinkedIn:", original_links.get("linkedin"))
            print("GitHub:", original_links.get("github"))
            print("Portfolio:", original_links.get("portfolio"))
            print("========================================")

            # -------------------------------------------------
            # Build answers text
            # -------------------------------------------------

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

            # -------------------------------------------------
            # Generate final resume
            # -------------------------------------------------

            ai_output = generate_resume_with_groq(
                enhanced_context,
                job
            )

            if ai_output.get("type") == "questions":

                return Response({
                    "error": "AI is still asking questions",
                    "details": ai_output
                }, status=400)

            # -------------------------------------------------
            # Resume generated
            # -------------------------------------------------

            if ai_output.get("type") == "resume":

                generated = GeneratedResume.objects.create(
                    user=request.user,
                    base_resume=resume,
                    job_application=job
                )

                resume_data = ai_output.get("content", {})

                # -------------------------------------------------
                # IMPORTANT:
                # Restore URLs from the ORIGINAL uploaded PDF.
                #
                # Never rely on the AI-generated values here because
                # the AI may return "Portfolio", "GitHub", etc.
                # -------------------------------------------------

                if original_links.get("linkedin"):
                    resume_data["linkedin"] = original_links["linkedin"]

                if original_links.get("github"):
                    resume_data["github"] = original_links["github"]

                if original_links.get("portfolio"):
                    resume_data["portfolio"] = original_links["portfolio"]

                print("========== FINAL RESUME LINKS ==========")
                print("LinkedIn:", resume_data.get("linkedin"))
                print("GitHub:", resume_data.get("github"))
                print("Portfolio:", resume_data.get("portfolio"))
                print("========================================")

                # -------------------------------------------------
                # Generate improvements summary
                # -------------------------------------------------

                improvements = generate_resume_improvements(
                    resume_text,
                    json.dumps(resume_data),
                    job
                )

                # -------------------------------------------------
                # Generate PDF
                # -------------------------------------------------

                pdf_url = generate_resume_pdf(
                    generated,
                    resume_data
                )

                return Response({
                    "type": "resume",
                    "message": "Resume generated successfully",
                    "generated_id": generated.id,
                    "job_id": job.id,
                    "pdf_url": pdf_url,
                    "improvements": improvements.get(
                        "improvements",
                        []
                    )
                })

            # -------------------------------------------------
            # Unexpected AI response
            # -------------------------------------------------

            return Response({
                "error": "Unexpected AI response",
                "details": ai_output
            }, status=400)

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
    print("Returned from AI:", data)
    print(type(data))

    return Response(data)

class DeleteGeneratedResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, resume_id):

        try:

            generated_resume = GeneratedResume.objects.get(
                id=resume_id,
                user = request.user
            )

            #Delete the pdf files if it exists
            if generated_resume.file:
                generated_resume.file.delete(save=False)

            #Delete database records
            generated_resume.delete()

            return Response({
                "message": "Generated resume deleted successfully"
            })

        except GeneratedResume.DoesNotExist:
            return Response({
                "error":"Resume Not Found"
            }, status=404)

class DeleteAllGeneratedResumesView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):

        resumes = GeneratedResume.objects.filter(
            user=request.user
        )

        count = resumes.count()

        for resume in resumes:

            if resume.file:
                resume.file.delete(save=False)

        resumes.delete()

        return Response({
            "message": f"{count} generated resumes deleted"
        })

class ResumeAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        generated_resumes = (
            GeneratedResume.objects.filter(
                user=user
            )
            .select_related("job_application")
        )

        total_generated = generated_resumes.count()

        # -----------------------------------
        # MOST TARGETED ROLE
        # -----------------------------------

        top_role = (
            generated_resumes
            .values("job_application__title")
            .annotate(count=Count("id"))
            .order_by("-count")
            .first()
        )

        most_targeted_role = (
            top_role["job_application__title"]
            if top_role and top_role["job_application__title"]
            else "No role data"
        )

        # -----------------------------------
        # MOST TARGETED COMPANY
        # -----------------------------------

        top_company = (
            generated_resumes
            .values("job_application__company")
            .annotate(count=Count("id"))
            .order_by("-count")
            .first()
        )

        most_targeted_company = (
            top_company["job_application__company"]
            if top_company and top_company["job_application__company"]
            else "No company data"
        )

        # -----------------------------------
        # UNIQUE ROLES TARGETED
        # -----------------------------------

        unique_roles_targeted = (
            generated_resumes
            .values("job_application__title")
            .distinct()
            .count()
        )

        # -----------------------------------
        # UNIQUE COMPANIES TARGETED
        # -----------------------------------

        unique_companies_targeted = (
            generated_resumes
            .values("job_application__company")
            .distinct()
            .count()
        )

        # -----------------------------------
        # MONTHLY GENERATION COUNT
        # -----------------------------------

        now = timezone.now()

        start_month = now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        monthly_generation_count = (
            generated_resumes
            .filter(created_at__gte=start_month)
            .count()
        )

        # -----------------------------------
        # TAILORED RESUME PERCENTAGE
        # -----------------------------------

        total_job_applications = (
            JobApplication.objects.filter(
                user=user
            ).count()
        )

        if total_job_applications > 0:

            tailored_resume_percentage = int(
                (
                    total_generated /
                    total_job_applications
                ) * 100
            )

        else:

            tailored_resume_percentage = 0

        tailored_resume_percentage = min(
            tailored_resume_percentage,
            100
        )

        # -----------------------------------
        # OPTIMIZATION IMPACT SCORE
        # -----------------------------------

        optimization_impact_score = 40

        optimization_impact_score += (
            total_generated * 4
        )

        optimization_impact_score += (
            unique_roles_targeted * 3
        )

        optimization_impact_score += (
            unique_companies_targeted * 2
        )

        optimization_impact_score = min(
            optimization_impact_score,
            100
        )

        # -----------------------------------
        # CAREER MOMENTUM
        # -----------------------------------

        recent_activity = (
            generated_resumes.filter(
                created_at__gte=now - timedelta(days=30)
            ).count()
        )

        if recent_activity >= 15:

            career_momentum = "Excellent"

        elif recent_activity >= 8:

            career_momentum = "High"

        elif recent_activity >= 3:

            career_momentum = "Growing"

        else:

            career_momentum = "Starting"

        # -----------------------------------
        # APPLICATION READINESS
        # -----------------------------------

        if optimization_impact_score >= 85:

            application_readiness = "Strong"

        elif optimization_impact_score >= 70:

            application_readiness = "Good"

        elif optimization_impact_score >= 50:

            application_readiness = "Developing"

        else:

            application_readiness = "Early Stage"

        # -----------------------------------
        # RESPONSE
        # -----------------------------------

        return Response({

            "total_generated":
                total_generated,

            "most_targeted_role":
                most_targeted_role,

            "most_targeted_company":
                most_targeted_company,

            "unique_roles_targeted":
                unique_roles_targeted,

            "unique_companies_targeted":
                unique_companies_targeted,

            "monthly_generation_count":
                monthly_generation_count,

            "tailored_resume_percentage":
                tailored_resume_percentage,

            "optimization_impact_score":
                optimization_impact_score,

            "career_momentum":
                career_momentum,

            "application_readiness":
                application_readiness
        })

class GenerateApplicationEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            job_id = request.data.get("job_id")
            resume_id = request.data.get("resume_id")

            resume = Resume.objects.get(
                id=resume_id,
                user=request.user
            )

            job = JobApplication.objects.get(
                id=job_id,
                user=request.user
            )

            resume_text = extract_text_from_pdf(
                resume.file.path
            )

            email_data = generate_application_email(
                resume_text,
                job
            )

            return Response(email_data)

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=500
            )

class InterviewPrepView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            generated_resume_id = request.data.get(
                "generated_resume_id"
            )

            if not generated_resume_id:

                return Response(
                    {
                        "error":
                        "generated_resume_id is required"
                    },
                    status=400
                )

            generated_resume = (
                GeneratedResume.objects.get(
                    id=generated_resume_id,
                    user=request.user
                )
            )

            if not generated_resume.file:

                return Response(
                    {
                        "error":
                        "Generated resume PDF not found"
                    },
                    status=400
                )

            job = generated_resume.job_application

            resume_text = extract_text_from_pdf(
                generated_resume.file.path
            )

            prep = generate_interview_prep(
                resume_text,
                job
            )

            return Response(prep)

        except GeneratedResume.DoesNotExist:

            return Response(
                {
                    "error":
                    "Generated resume not found"
                },
                status=404
            )

        except Exception as e:

            import traceback

            traceback.print_exc()

            return Response(
                {
                    "error": str(e)
                },
                status=500
            )

class StartMockInterviewView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            generated_resume_id = request.data.get(
                "generated_resume_id"
            )

            generated_resume = (
                GeneratedResume.objects.get(
                    id=generated_resume_id,
                    user=request.user
                )
            )

            resume_text = extract_text_from_pdf(
                generated_resume.file.path
            )

            question_data = (
                generate_first_interview_question(
                    resume_text,
                    generated_resume.job_application
                )
            )

            session = (
                MockInterviewSession.objects.create(
                    user=request.user,
                    generated_resume=generated_resume,
                    current_question=
                        question_data["question"],
                    current_category=
                        question_data["category"]
                )
            )

            return Response({

                "session_id":
                    session.id,

                "question":
                    question_data["question"],

                "category":
                    question_data["category"]

            })

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=500
            )

class AnswerMockInterviewView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            session_id = request.data.get(
                "session_id"
            )

            answer = request.data.get(
                "answer"
            )

            session = (
                MockInterviewSession.objects.get(
                    id=session_id,
                    user=request.user
                )
            )

            generated_resume = (
                session.generated_resume
            )

            resume_text = extract_text_from_pdf(
                generated_resume.file.path
            )

            result = evaluate_interview_answer(
                question=session.current_question,
                category=session.current_category,
                answer=answer,
                resume_text=resume_text,
                job=generated_resume.job_application
            )

            MockInterviewMessage.objects.create(
                session=session,
                question=session.current_question,
                category=session.current_category,
                answer=answer,
                score=result["score"],
                technical_score=result["technical_score"],
                communication_score=result["communication_score"],
                confidence_score=result["confidence_score"],
                feedback=result["feedback"],
                ideal_answer=result["ideal_answer"]
            )

            session.total_score += (
                result["score"]
            )

            session.questions_answered += 1

            session.current_question = (
                result["next_question"]
            )

            session.current_category = (
                result["next_category"]
            )

            session.save()

            average_score = (
                session.total_score /
                session.questions_answered
            )

            return Response({

                "score":
                    result["score"],

                "technical_score":
                    result["technical_score"],

                "communication_score":
                    result["communication_score"],

                "confidence_score":
                    result["confidence_score"],

                "feedback":
                    result["feedback"],

                "ideal_answer":
                    result["ideal_answer"],

                "next_question":
                    result["next_question"],

                "next_category":
                    result["next_category"],

                "average_score":
                    round(
                        average_score,
                        1
                    )

            })

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=500
            )
