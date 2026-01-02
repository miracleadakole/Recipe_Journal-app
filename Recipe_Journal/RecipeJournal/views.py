from rest_framework.decorators import permission_classes, api_view, action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import UserRegistrationSerializer, IngredientSerializer, RecipeSerializer, RecipeIngredientSerializer
from .models import Ingredient, Recipe, RecipeIngredient
from rest_framework.exceptions import PermissionDenied, ValidationError
import requests
from django.conf import settings


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

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        """
        POST /recipes/{id}/analyze/
        """
        recipe = self.get_object()

        # Get ingredient names linked to this recipe
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

        if not recipe_ingredients.exists():
            return Response({
                "recipe": recipe.title,
                "status": "No ingredients added to recipe."
            }, status=status.HTTP_400_BAD_REQUEST)

        ingredient_lines = []

        for ri in recipe.recipe_ingredients.all():
            qty = ri.quantity or ""
            unit = ri.unit or ""
            name = ri.ingredient.name

            ingredient_lines.append(
                f"{qty} {unit} {name}".strip()
            )

        summary = []

        # Example rules (simplified):
        for ri in recipe.recipe_ingredients.all():
            name = ri.ingredient.name.lower()
            if name in ['chicken', 'egg', 'tofu', 'beans']:
                summary.append("protein-rich")
            if name in ['carrot', 'broccoli', 'spinach', 'beans']:
                summary.append("high-fiber")
            if name in ['rice', 'potato', 'bread']:
                summary.append("high-carb")


        url = "https://api.edamam.com/api/nutrition-details"

        params = {
            "app_id": settings.EDAMAM_APP_ID,
            "app_key": settings.EDAMAM_APP_KEY,
        }

        payload = {
            "title": recipe.title,
            "ingr": ingredient_lines
        }

        try:
            response = requests.post(url, params=params, json=payload)

            data = response.json()

            if response.status_code != 200:
                return Response({
                    "status": "Edamam API error",
                    "sent": ingredient_lines,
                    "detail": data
                }, status=response.status_code)

            return Response({
                "recipe": recipe.title,
                "ingredients_sent": ingredient_lines,
                "calories": data.get("calories"),
                "dietLabels": data.get("dietLabels"),
                "healthLabels": data.get("healthLabels"),
                "totalNutrients": data.get("totalNutrients"),
                "summary": list(set(summary)), 
                "status": "Nutrition successfully analyzed"
            })

        except Exception as e:
            return Response({
                "error": str(e),
                "status": "Request failed"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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












        