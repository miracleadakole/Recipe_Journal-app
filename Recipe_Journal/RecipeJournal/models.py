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

class Ingredient(models.Model):
    """
    Represents an ingredient for a recipe.
    """
    name = models.CharField(max_length=200, unique=True, help_text="Name of the ingredient, e.g., 'Tomato'")
    description = models.TextField(blank=True, help_text="Optional description of the ingredient.")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingredients')

    class Meta:
        ordering = ['name'] # Order ingredients alphabetically by name

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200, help_text="Recipe title")
    description = models.TextField(blank=True, help_text="Optional recipe description")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # newest recipes first

    def __str__(self):
        return self.title 
