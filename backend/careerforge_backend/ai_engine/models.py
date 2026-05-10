from django.db import models
from django.conf import settings

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
        max_length=255,
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

