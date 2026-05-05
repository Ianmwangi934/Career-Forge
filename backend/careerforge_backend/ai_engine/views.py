from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from resumes.models import Resume
from job_applications.models import JobApplication, GeneratedResume

from .utils import extract_text_from_pdf
from .grok_client import generate_resume_with_groq



# Create your views here.

class GenerateResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
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

        
        # Call Grok
        ai_output = generate_resume_with_grok(resume_text, job)

        # 🔥 CASE 1: AI asks a question
        if ai_output.get("type") == "question":
            return Response(ai_output, status=200)


        # 🔥 CASE 2: AI returns resume
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


        # 🔥 CASE 3: AI failed
        return Response({
            "error": "AI failed",
            "details": ai_output
        }, status=500)
