from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import welcome_user, SignupView, IngredientViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('Welcome/', welcome_user),
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]