from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """
    Custom User Model.
    The fields 'username', 'password', 'first_name', 'last_name', and 'email'
    are already inherited from AbstractUser, so you don't need to define them.
    """
    
    # Add any extra fields you want here.
    # For example, a bio for the user's profile.
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username