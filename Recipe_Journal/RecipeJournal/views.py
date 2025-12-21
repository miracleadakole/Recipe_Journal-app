from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer


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