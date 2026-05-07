from rest_framework import serializers
from .models import AIQuestionSession, AIQuestion


class AIQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIQuestion
        fields = [
            "id",
            "question",
            "options",
            "answer",
            "order"
        ]


class AIQuestionSessionSerializer(serializers.ModelSerializer):

    questions = AIQuestionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = AIQuestionSession
        fields = [
            "id",
            "completed",
            "created_at",
            "questions"
        ]