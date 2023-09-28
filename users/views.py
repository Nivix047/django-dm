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

# Endpoint for user registration with token-based authentication


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

# Endpoint for user login with token-based authentication


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

# Endpoint to list all users and create a new user


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # Allowing any for registration

# Endpoint to retrieve, update, and delete a specific user


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

# Below code is in APIview format which is designed for more complex logic and customization.
# Above code is in generics format which is designed for simple CRUD operations.
# Creating a user doesn't require any complex logic.

# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token

# from .models import CustomUser
# from .serializers import CustomUserSerializer

# class RegisterView(APIView):
#     # Permission set to allow any user (including unauthenticated) to access this view
#     permission_classes = [AllowAny]

#     def post(self, request):
#         # Serialize request data to validate it
#         serializer = CustomUserSerializer(data=request.data)

#         # Check if the serialized data is valid
#         if serializer.is_valid():
#             # Save the user instance
#             user = serializer.save()

#             # Retrieve existing token for the user or create a new one if it doesn't exist
#             token, _ = Token.objects.get_or_create(user=user)

#             # Return the token and user id in the response
#             return Response({'token': token.key, 'user_id': user.pk}, status=status.HTTP_201_CREATED)

#         # If the serialized data isn't valid, return an error response
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_view(request):
#     username = request.data.get("username")
#     password = request.data.get("password")

#     # Check if both username and password are provided.
#     if not username or not password:
#         return Response({"error": "Username and password are required"}, status=400)

#     # Try to authenticate the user with the provided credentials.
#     user = authenticate(username=username, password=password)

#     # If the user is authenticated successfully...
#     if user:
#         # Create a token for the user or get the existing one.
#         token, created = Token.objects.get_or_create(user=user)
#         # Return the token and user ID as a response.
#         return Response({"token": token.key, "user_id": user.pk})
#     # If authentication fails, return an error message.
#     else:
#         return Response({"error": "Invalid Credentials"}, status=401)

# class UserListCreateView(APIView):
#     # Allows any user (including unauthenticated) to access this view
#     permission_classes = [AllowAny]

#     def get(self, request):
#         # Fetch all users
#         users = CustomUser.objects.all()
#         serializer = CustomUserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         # Serialize request data to validate it
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             Token.objects.get_or_create(user=user)  # Creates a token for the user
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserRetrieveUpdateDestroyView(APIView):
#     # Ensures that only authenticated users can access this view
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             user = CustomUser.objects.get(pk=pk)
#             serializer = CustomUserSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, pk):
#         try:
#             user = CustomUser.objects.get(pk=pk)
#             serializer = CustomUserSerializer(user, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, pk):
#         try:
#             user = CustomUser.objects.get(pk=pk)
#             user.delete()
#             return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
