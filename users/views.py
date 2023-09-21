from django.shortcuts import render
import logging
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from .models import CustomUser
from .serializers import CustomUserSerializer

# Initialize the logger for this module
logger = logging.getLogger(__name__)

# Define a ViewSet for the CustomUser model.
# ViewSets are a type of class-based view provided by DRF that provide CRUD operations by default.


class CustomUserViewSet(viewsets.ModelViewSet):
    # Define the default queryset that this ViewSet will operate on.
    queryset = CustomUser.objects.all()

    # Define the serializer that this ViewSet will use to convert between Django models and JSON representations.
    serializer_class = CustomUserSerializer

    # Set default permission class
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # If the action is 'register', then allow any user
        if self.action == 'register':
            permission_classes = [AllowAny]
        else:
            # For other actions (like 'list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'),
            # only allow authenticated users
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # Define a custom action for this ViewSet. This action will handle user registration.
    @action(detail=False, methods=['POST'])
    def register(self, request):
        # Log an informational message whenever this endpoint is accessed.
        logger.info("Register endpoint accessed.")

        # Deserialize the incoming request data into a CustomUser object.
        serializer = self.get_serializer(data=request.data)

        # Validate the deserialized data.
        if serializer.is_valid():
            # If valid, save the new user to the database.
            user = serializer.save()

            # Create a token for the new user or get the existing one.
            token, created = Token.objects.get_or_create(user=user)

            # Return the token and user ID as a response.
            return Response({'token': token.key, 'user_id': user.pk}, status=status.HTTP_201_CREATED)

        # If the data is not valid, return the errors.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Define a function-based view to handle user login.


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    # Extract username and password from the request data.
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
