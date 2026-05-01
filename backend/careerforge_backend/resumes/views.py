from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Resume
from .serializers import ResumeSerializer

# Create your views here.
class ResumeUploadView(CreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes =[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class ResumeListView(ListAPIView):
    serializer_class = ResumeSerializer
    permission_classes =  [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
