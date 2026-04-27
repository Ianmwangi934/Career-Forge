from django.urls import path
from .views import RegisterView, LoginView, UserProfile

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserProfile.as_view(), name='profile')
]