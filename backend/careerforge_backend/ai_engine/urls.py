from django.urls import path
from .views import GenerateResumeView, AnswerAIQuestionView, career_news, resume_insights, DeleteGeneratedResumeView, DeleteAllGeneratedResumesView,ResumeAnalyticsView, GenerateApplicationEmailView, InterviewPrepView, StartMockInterviewView, AnswerMockInterviewView

urlpatterns = [
    path("generate/" ,GenerateResumeView.as_view()),
    path("answer-question/", AnswerAIQuestionView.as_view()),
    path("career-news/",career_news),
    path("resume-insights/",resume_insights),
    path("generated-resumes/<int:resume_id>/delete/", DeleteGeneratedResumeView.as_view()),
    path("generated-resumes/delete-all/", DeleteAllGeneratedResumesView.as_view()),
    path("resume-analytics/", ResumeAnalyticsView.as_view()),
    path("generate-email/",GenerateApplicationEmailView.as_view()),
    path("interview-prep/",InterviewPrepView.as_view()),
    path("mock-interview/start/",StartMockInterviewView.as_view()),
    path("mock-interview/answer/",AnswerMockInterviewView.as_view())
]