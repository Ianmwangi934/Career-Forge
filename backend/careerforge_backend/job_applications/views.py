from django.shortcuts import render
from rest_framework import generics, permissions
from .models import JobApplication
from .serializers import JobApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import (
    JobApplication,
    GeneratedResume
)

from .serializers import (
    JobApplicationSerializer,
    GeneratedResumeSerializer
)

# Create your views here.
class JobApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GeneratedResumeListView(
    generics.ListAPIView
):

    serializer_class = GeneratedResumeSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GeneratedResume.objects.filter(
            user=self.request.user,
            file__isnull=False
        ).exclude(
            file=""
        ).order_by(
            "-created_at"
        )