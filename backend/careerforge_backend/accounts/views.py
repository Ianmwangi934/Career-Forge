from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .serializers import RegisterSerializer
from rest_framework

# Create your views here.
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

class UserProfile(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
