from django.urls import path
from .views import welcome_user
from .views import SignupView


urlpatterns = [
    path('Welcome/', welcome_user),
    path('signup/', SignupView.as_view(), name='signup'),
]