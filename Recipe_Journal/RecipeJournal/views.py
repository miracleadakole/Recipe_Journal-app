from rest_framework.decorators import permission_classes, api_view, action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import UserRegistrationSerializer, IngredientSerializer, RecipeSerializer, RecipeIngredientSerializer
from .models import Ingredient, Recipe, RecipeIngredient
from rest_framework.exceptions import PermissionDenied, ValidationError
import requests


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def welcome_user(request):
    return Response({
        "message": f"Welcome {request.user.username}"
    })

class SignupView(APIView):
    """
    This view handles user registration.
    Anyone can access this endpoint.
    """
    permission_classes = [] # No authentication required to sign up

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully!',
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IngredientViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing ingredient instances.
    Provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated] # <-- Secure this endpoint

    def get_queryset(self):
        """
        This view should return a list of all the ingredients
        for the currently authenticated user.
        """
        return Ingredient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the created_by field to the logged-in user.
        """
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'], url_path='benefits')
    def benefits(self, request, pk=None):
        ingredient = self.get_object()

        mock_data = {
        "ingredient": ingredient.name,
        "benefits": [
            "Rich in vitamins",
            "Supports immunity",
            "Good for digestion"
        ]
    }

        return Response(mock_data, status=status.HTTP_200_OK)

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return recipes for the logged-in user
        return Recipe.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Automatically link recipe to logged-in user
        serializer.save(created_by=self.request.user)

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeIngredientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow access to ingredients in recipes belonging to logged-in user
        return RecipeIngredient.objects.filter(recipe__created_by=self.request.user)

    def perform_create(self, serializer):
        # Optional: validate that the recipe belongs to the logged-in user
        recipe = serializer.validated_data['recipe']
        if recipe is None:
            raise ValidationError("Recipe field is required.")

        # Ensure the recipe belongs to current user
        if recipe.created_by != self.request.user:
            raise PermissionDenied(
                "You cannot add ingredients to someone else's recipe."
            )

        serializer.save()












        