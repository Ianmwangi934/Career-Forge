from django.urls import path
from .views import JobApplicationListCreateView, GeneratedResumeListView

urlpatterns = [
    path("", JobApplicationListCreateView.as_view(), name="appliactions"),
    path("generated-resumes/",GeneratedResumeListView.as_view(),name="generated-resumes")
]