from django.shortcuts import render
from rest_framework import generics, permissions
from .models import JobAppliaction
from .serializers import JobApplicationSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class JobAppliactionListCreateView(generics.ListCreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobAppliaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
