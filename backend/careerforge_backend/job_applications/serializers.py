from rest_framework import serializers
from .models import JobAppliaction

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAppliaction
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