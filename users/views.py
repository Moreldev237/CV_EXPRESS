from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
import os

# Pour l'envoi d'e-mails (non implémenté ici, juste pour l'exemple)
# from django.core.mail import send_mail

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    UpdateProfileSerializer,
    ProfileImageUploadSerializer,
    OTPVerificationSerializer,
    OTPRequestSerializer
)
from .models import OTP


class RegisterView(APIView):
    """
    Endpoint pour l'inscription des utilisateurs.
    Crée un nouveau compte utilisateur inactif et envoie un code OTP par e-mail
    pour vérification avant activation.
    """
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        tags=['Authentification'],
        operation_id='Enregistrer un utilisateur',
        operation_description="Enregistre un nouvel utilisateur avec e-mail et mot de passe. "
                              "L'e-mail servira d'identifiant unique. "
                              "Un code OTP est envoyé par e-mail pour activer le compte.",
        request_body=RegisterSerializer,
        consumes=['application/x-www-form-urlencoded'],
        responses={
            201: openapi.Response(
                description='Utilisateur enregistré avec succès',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message de confirmation'),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='Détails de l\'utilisateur')
                    }
                )
            ),
            400: 'Erreur de validation'
        },
        security=[]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Utilisateur enregistré avec succès. Veuillez vérifier votre e-mail pour le code de validation.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyRegistrationOTPView(APIView):
    """
    Endpoint pour vérifier le code OTP et activer le compte utilisateur.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        tags=['Authentification'],
        operation_id='Vérifier OTP',
        operation_description='Vérifie le code OTP envoyé par e-mail. Si le code est valide et non expiré, le compte est activé et les tokens JWT sont renvoyés.',
        request_body=OTPVerificationSerializer,
        consumes=['application/x-www-form-urlencoded'],
        responses={
            200: openapi.Response(
                description='Compte activé avec succès',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
            400: 'Code invalide ou expiré',
            404: 'Utilisateur non trouvé'
        },
        security=[]
    )
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    return Response({'error': 'Ce compte est déjà activé.'}, status=status.HTTP_400_BAD_REQUEST)
                
                otp = OTP.objects.filter(user=user, code=otp_code, is_verified=False).first()
                
                if not otp or otp.is_expired:
                    return Response({'error': 'Code OTP invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Activer l'utilisateur
                user.is_active = True
                user.save()
                
                # Marquer l'OTP comme utilisé
                otp.is_verified = True
                otp.save()
                
                # Générer les tokens pour connexion immédiate
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'message': 'Compte activé avec succès.',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestNewOTPView(APIView):
    """
    Endpoint pour demander un nouveau code OTP si le précédent a expiré.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        tags=['Authentification'],
        operation_id='Renvoyer OTP',
        operation_description='Génère et envoie un nouveau code OTP à l\'adresse e-mail fournie si le compte n\'est pas encore activé.',
        request_body=OTPRequestSerializer,
        consumes=['application/x-www-form-urlencoded'],
        responses={
            200: openapi.Response(
                description='Nouveau code OTP envoyé',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: 'Erreur de validation ou compte déjà actif',
            404: 'Utilisateur non trouvé'
        },
        security=[]
    )
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    return Response({'error': 'Ce compte est déjà activé.'}, status=status.HTTP_400_BAD_REQUEST)
                
                import random
                otp_code = str(random.randint(100000, 999999))
                expires_at = timezone.now() + timezone.timedelta(minutes=10)
                OTP.objects.create(user=user, code=otp_code, expires_at=expires_at)
                
                # En production, envoyer l'email ici
                logger = logging.getLogger(__name__)
                logger.info(f"New OTP generated for {user.email}: {otp_code}")
                
                return Response({'message': 'Un nouveau code OTP a été envoyé par e-mail.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    Endpoint pour récupérer le profil de l'utilisateur actuel.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        tags=['Profil'],
        operation_id='Obtenir le profil',
        operation_description='Récupère les informations du profil de l\'utilisateur actuellement authentifié.',
        responses={
            200: openapi.Response(
                description='Profil récupéré avec succès',
                schema=UserSerializer
            ),
            401: 'Non autorisé'
        },
        security=[{'Bearer': []}]
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UpdateProfileView(APIView):
    """
    Endpoint pour mettre à jour le profil de l'utilisateur actuel.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        tags=['Profil'],
        operation_id='Mettre à jour le profil',
        operation_description='Met à jour les informations du profil de l\'utilisateur authentifié. Tous les champs sont optionnels.',
        request_body=UpdateProfileSerializer,
        consumes=['application/x-www-form-urlencoded'],
        responses={
            200: openapi.Response(
                description='Profil mis à jour avec succès',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='Profil mis à jour')
                    }
                )
            ),
            400: 'Validation Error',
            401: 'Unauthorized'
        },
        security=[{'Bearer': []}]
    )
    def put(self, request):
        serializer = UpdateProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profil mis à jour avec succès.',
                'user': UserSerializer(request.user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadProfileImageView(APIView):
    """
    Endpoint pour télécharger une image de profil.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        tags=['Profil'],
        operation_id='Télécharger l\'image de profil',
        operation_description='Télécharge une nouvelle image de profil. Formats supportés: jpg, jpeg, png, gif. Taille max: 5Mo.',
        request_body=ProfileImageUploadSerializer,
        consumes=['multipart/form-data'],
        responses={
            200: openapi.Response(
                description='Image de profil téléchargée avec succès',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'profile_image': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: 'Validation Error',
            401: 'Unauthorized'
        },
        security=[{'Bearer': []}]
    )
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
                'message': 'Image de profil téléchargée avec succès.',
                'profile_image': request.user.profile_image.url
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
