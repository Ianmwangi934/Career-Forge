from rest_framework import serializers
from .models import JobApplication
from .models import GeneratedResume

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


    def validate(self, data):
        if not any([
            data.get("description"),
            data.get("responsibilities"),
            data.get("skills"),
        ]):
            raise serializers.ValidationError(
                "At least one field (description, responsibilities, skills) must be provided."
            )

        return data

class GeneratedResumeSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job_application.title")
    company = serializers.CharField(source="job_application.company")

    class Meta:
        model = GeneratedResume

        fields = [
            "id",
            "file",
            "job_title",
            "company",
            "created_at"
        ]