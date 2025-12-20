from django.urls import path
from .views import welcome_user

urlpatterns = [
    path('Welcome/', welcome_user)
]