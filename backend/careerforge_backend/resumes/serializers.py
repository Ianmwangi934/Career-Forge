from rest_framework import serializers
from .models import Resume

#Converting response to Json and incoming request back to Python object for validation
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "file", "title", "uploaded_at"]
        read_only_fields =["id", "uploaded_at"]