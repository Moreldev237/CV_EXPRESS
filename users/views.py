from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
import os

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    UpdateProfileSerializer,
    ProfileImageUploadSerializer
)


class RegisterView(APIView):
    """
    API endpoint for user registration.
    
    POST /api/users/register/
    
    Request Body:
    {
        "email": "user@example.com",
        "username": "username",
        "password": "password123",
        "password_confirm": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    Success Response (201):
    {
        "message": "User registered successfully.",
        "user": {
            "id": 1,
            "email": "user@example.com",
            "username": "username",
            "first_name": "John",
            "last_name": "Doe"
        }
    }
    
    Error Response (400):
    {
        "email": ["This email is already registered."],
        "username": ["A user with that username already exists."]
    }
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    API endpoint to get current user profile.
    
    GET /api/users/profile/
    
    Headers:
    Authorization: Bearer <access_token>
    
    Success Response (200):
    {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "John",
        "last_name": "Doe",
        "profile_image": "/media/profile_images/photo.jpg",
        "bio": "Bio text",
        "phone": "+1234567890",
        ...
    }
    
    Error Response (401):
    {
        "detail": "Authentication credentials were not provided."
    }
    """
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UpdateProfileView(APIView):
    """
    API endpoint to update current user profile.
    
    PUT /api/users/profile/update/
    
    Headers:
    Authorization: Bearer <access_token>
    
    Request Body:
    {
        "first_name": "John",
        "last_name": "Doe",
        "bio": "Updated bio",
        "phone": "+1234567890",
        "address": "123 Main St",
        "occupation": "Developer",
        "company": "Tech Corp",
        "website": "https://example.com",
        "linkedin": "https://linkedin.com/in/user",
        "github": "https://github.com/user"
    }
    
    Success Response (200):
    {
        "message": "Profile updated successfully.",
        "user": { ... updated user data ... }
    }
    
    Error Response (400):
    {
        "field_name": ["Error message"]
    }
    """
    def put(self, request):
        serializer = UpdateProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully.',
                'user': UserSerializer(request.user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadProfileImageView(APIView):
    """
    API endpoint to upload profile image.
    
    POST /api/users/profile/upload-image/
    
    Headers:
    Authorization: Bearer <access_token>
    Content-Type: multipart/form-data
    
    Request Body (form-data):
    profile_image: <image_file>
    
    Success Response (200):
    {
        "message": "Profile image uploaded successfully.",
        "profile_image": "/media/profile_images/username_photo.jpg"
    }
    
    Error Response (400):
    {
        "profile_image": ["Error message"]
    }
    """
    def post(self, request):
        serializer = ProfileImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Delete old profile image if exists and not default
            if request.user.profile_image:
                try:
                    old_image_path = request.user.profile_image.path
                    if os.path.exists(old_image_path) and 'default' not in old_image_path:
                        os.remove(old_image_path)
                except Exception:
                    pass
            
            # Save new profile image
            request.user.profile_image = serializer.validated_data['profile_image']
            request.user.save()
            
            return Response({
                'message': 'Profile image uploaded successfully.',
                'profile_image': request.user.profile_image.url
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    API endpoint for user logout.
    
    POST /api/users/auth/logout/
    
    Headers:
    Authorization: Bearer <refresh_token>
    
    Success Response (200):
    {
        "message": "Logout successful."
    }
    """
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                'message': 'Logout successful.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Error during logout.'
            }, status=status.HTTP_400_BAD_REQUEST)
