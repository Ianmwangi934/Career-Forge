from django.urls import path
from .views import ResumeUploadView, ResumeListView,ResumeDeleteView

urlpatterns = [
    path("upload/", ResumeUploadView.as_view(), name="upload-resume"),
    path("", ResumeListView.as_view(), name="list-resumes"),
    path("<int:pk>/delete/", ResumeDeleteView.as_view(), name="delete-resume"),
]