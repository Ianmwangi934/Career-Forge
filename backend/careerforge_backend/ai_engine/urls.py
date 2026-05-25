from django.urls import path
from .views import GenerateResumeView, AnswerAIQuestionView, career_news, resume_insights, DeleteGeneratedResumeView, DeleteAllGeneratedResumesView,ResumeAnalyticsView

urlpatterns = [
    path("generate/" ,GenerateResumeView.as_view()),
    path("answer-question/", AnswerAIQuestionView.as_view()),
    path("career-news/",career_news),
    path("resume-insights/",resume_insights),
    path("generated-resumes/<int:resume_id>/delete/", DeleteGeneratedResumeView.as_view()),
    path("generated-resumes/delete-all/", DeleteAllGeneratedResumesView.as_view()),
    path("resume-analytics/", ResumeAnalyticsView.as_view())
]