from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    file = models.FileField(upload_to="resumes/")
    title = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.title or self.file.name}"
