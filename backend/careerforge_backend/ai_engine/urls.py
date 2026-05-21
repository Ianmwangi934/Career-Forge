from django.urls import path
from .views import GenerateResumeView, AnswerAIQuestionView, career_news

urlpatterns = [
    path("generate/" ,GenerateResumeView.as_view()),
    path("answer-question/", AnswerAIQuestionView.as_view()),
    path("career-news/",career_news)
]