from django.urls import path
from .views import GenerateResumeView, AnswerAIQuestionView

urlpatterns = [
    path("generate/" ,GenerateResumeView.as_view()),
    path("answer-question/", AnswerAIQuestionView.as_view())
]