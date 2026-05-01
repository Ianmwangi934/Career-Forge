from django.urls import path
from .views import ResumeUploadView, ResumeListView

urlpatterns = [
    path("upload/", ResumeUploadView.as_view(), name="upload-resume"),
    path("", ResumeListView.as_view(), name="list-resumes"),
]