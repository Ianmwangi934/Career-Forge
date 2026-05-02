from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Resume
from .serializers import ResumeSerializer
from rest_framework import generics

# Create your views here.
#Uploading the CV
class ResumeUploadView(CreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes =[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

#Viewing or listing the CVs
class ResumeListView(ListAPIView):
    serializer_class = ResumeSerializer
    permission_classes =  [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

#Deleting the CV
class ResumeDeleteView(generics.DestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
