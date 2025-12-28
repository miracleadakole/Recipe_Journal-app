from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Ingredient, Recipe, RecipeIngredient

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredient model.
    """
    # We add a read-only field to show the username of the creator
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Ingredient
        # List the fields we want in our API responses
        fields = ['id', 'name', 'description', 'created_by', 'created_by_username']
        # We'll set the 'created_by' field automatically in the view
        read_only_fields = ['created_by', 'created_by_username']

class RecipeSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'created_by', 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_by_username', 'created_at', 'updated_at']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    recipe_title = serializers.CharField(source='recipe.title', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'recipe', 'recipe_title', 'ingredient', 'ingredient_name', 'quantity', 'unit']