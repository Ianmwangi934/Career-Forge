from django.urls import path
from .views import JobAppliactionListCreateView

urlpatterns = [
    path("", JobAppliactionListCreateView.as_view(), name="appliactions")
]