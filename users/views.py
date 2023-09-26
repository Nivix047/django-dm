from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import CustomUserSerializer


class RegisterView(APIView):
    # Permission set to allow any user (including unauthenticated) to access this view
    permission_classes = [AllowAny]

    def post(self, request):
        # Serialize request data to validate it
        serializer = CustomUserSerializer(data=request.data)

        # Check if the serialized data is valid
        if serializer.is_valid():
            # Save the user instance
            user = serializer.save()
            
            # Retrieve existing token for the user or create a new one if it doesn't exist
            token, _ = Token.objects.get_or_create(user=user)
            
            # Return the token and user id in the response
            return Response({'token': token.key, 'user_id': user.pk}, status=status.HTTP_201_CREATED)
        
        # If the serialized data isn't valid, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    # Check if both username and password are provided.
    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    # Try to authenticate the user with the provided credentials.
    user = authenticate(username=username, password=password)

    # If the user is authenticated successfully...
    if user:
        # Create a token for the user or get the existing one.
        token, created = Token.objects.get_or_create(user=user)
        # Return the token and user ID as a response.
        return Response({"token": token.key, "user_id": user.pk})
    # If authentication fails, return an error message.
    else:
        return Response({"error": "Invalid Credentials"}, status=401)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # Allowing any for registration

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.get_or_create(user=user)  # This creates a token for the user

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

