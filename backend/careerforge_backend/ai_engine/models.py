from django.db import models
from django.conf import settings
from job_applications.models import GeneratedResume

User = settings.AUTH_USER_MODEL

# Create your models here.
class AIQuestionSession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ai_sessions"
    )

    resume = models.ForeignKey(
        "resumes.Resume",
        on_delete=models.CASCADE,
        related_name="ai_sessions"
    )

    job_application = models.ForeignKey(
        "job_applications.JobApplication",
        on_delete=models.CASCADE,
        related_name="ai_sessions"
    )
    answer = models.TextField(
        blank=True,
        null=True
    )

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - AI Session"


class AIQuestion(models.Model):

    session = models.ForeignKey(
        AIQuestionSession,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()

    options = models.JSONField(default=list)

    answer = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question {self.order} - Session {self.session.id}"


class MockInterviewSession(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    generated_resume = models.ForeignKey(
        GeneratedResume,
        on_delete=models.CASCADE
    )

    current_question = models.TextField()

    current_category = models.CharField(
        max_length=100
    )

    total_score = models.FloatField(
        default=0
    )

    questions_answered = models.IntegerField(
        default=0
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Interview #{self.id}"


class MockInterviewMessage(models.Model):

    session = models.ForeignKey(
        MockInterviewSession,
        related_name="messages",
        on_delete=models.CASCADE
    )

    question = models.TextField()

    category = models.CharField(
        max_length=100
    )

    answer = models.TextField()

    score = models.FloatField()

    technical_score = models.FloatField()

    communication_score = models.FloatField()

    confidence_score = models.FloatField()

    feedback = models.TextField()

    ideal_answer = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Message #{self.id}"

