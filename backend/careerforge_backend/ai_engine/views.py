from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from resumes.models import Resume
from job_applications.models import JobApplication, GeneratedResume
from .models import AIQuestionSession
from .models import AIQuestion

from .utils import extract_text_from_pdf
from .grok_client import (
    generate_resume_with_groq,
    analyze_resume_for_questions
)



# Create your views here.

class GenerateResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("GenerateResumeView HIT")
        print(request.data)
        resume_id = request.data.get("resume_id")
        job_id = request.data.get("job_id")

        try:
            resume = Resume.objects.get(id=resume_id, user=request.user)
            job = JobApplication.objects.get(id=job_id, user=request.user)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=404)

        except JobApplication.DoesNotExist:
            return Response({"error": "Job not found"}, status=404)
        #  Extract text
        resume_text = extract_text_from_pdf(resume.file.path)

        
        # STEP 1 — Analyze resume for ATS gaps
        analysis = analyze_resume_for_questions(
            resume_text,
            job
        )

        # CASE 1 — AI generated follow-up questions
        if analysis.get("type") == "questions":

            session = AIQuestionSession.objects.create(
                user=request.user,
                resume=resume,
                job_application=job
            )

            questions_data = analysis.get("questions", [])

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
            }, status=200)

        # STEP 2 — No questions needed → generate resume immediately
        ai_output = generate_resume_with_groq(
            resume_text,
            job
        )

        #  CASE 2: AI returns resume
        if ai_output.get("type") == "resume":
            generated = GeneratedResume.objects.create(
                user=request.user,
                base_resume=resume,
                job_application=job,
                file=""  # later PDF
            )

            return Response({
                "message": "Resume generated",
                "content": ai_output.get("content"),
                "generated_id": generated.id
            }, status=200)


        #  CASE 3: AI failed
        return Response({
            "error": "AI failed",
            "details": ai_output
        }, status=500)

class AnswerAIQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        session_id = request.data.get("session_id")
        answer = request.data.get("answer")

        try:
            session = AIQuestionSession.objects.get(
                id = session_id,
                user = request.user
            )

        except AIQuestionSession.DoesNotExist:
            return Response(
                {"error": "Session not found"},
                status=404
            )

        #Save Answer
        session.answer = answer
        session.completed = True
        session.save()

        # Retrieve original data
        resume = session.resume
        job = session.job_application

        # Extract resume text again
        resume_text = extract_text_from_pdf(resume.file.path)

        #  Append follow-up answer
        enhanced_context = f"""

FOLLOW-UP USER ANSWER:
{answer}

ORIGINAL RESUME:
{resume_text}
"""

        # Call AI again
        ai_output = generate_resume_with_groq(
            enhanced_context,
            job
        )

        # Final response
        if ai_output.get("type") == "resume":

            generated = GeneratedResume.objects.create(
                user=request.user,
                base_resume=resume,
                job_application=job,
                file=""  # PDF later
            )

            return Response({
                "message": "Resume generated successfully",
                "content": ai_output.get("content"),
                "generated_id": generated.id
            })

        return Response({
            "error": "AI failed",
            "details": ai_output
        }, status=500)
