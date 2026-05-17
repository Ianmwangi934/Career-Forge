from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.
class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "applications")
    title = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Untitled Application"

class GeneratedResume(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="generated_resumes"
    )

    base_resume = models.ForeignKey(
        "resumes.Resume",
        on_delete=models.CASCADE,
        related_name="generated_versions"
    )

    job_application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="generated_resumes"
    )

    file = models.FileField(
        upload_to="generated_resumes/",
        blank=False,
        null=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.job_application.title} @ {self.job_application.company}"
