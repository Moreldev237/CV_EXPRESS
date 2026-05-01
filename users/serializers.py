from rest_framework import serializers
from .models import User, OTP
from django.utils import timezone
from django.utils.crypto import get_random_string
import random

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model - Read operations
    """
    full_name = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'profile_image', 'bio', 'phone', 'address', 'date_of_birth',
            'occupation', 'company', 'website', 'linkedin', 'github',
            'completion_percentage', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_completion_percentage(self, obj):
        """
        Calcule le pourcentage de complétion du profil basé sur les champs importants.
        """
        fields_to_check = [
            'first_name', 'last_name', 'profile_image', 'bio', 
            'phone', 'address', 'occupation', 'linkedin'
        ]
        if not fields_to_check:
            return 0
        
        filled_fields = 0
        for field in fields_to_check:
            value = getattr(obj, field)
            if value and value != 'default_profile.png':
                filled_fields += 1
        
        percentage = (filled_fields / len(fields_to_check)) * 100
        return round(percentage, 2)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for User registration
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 
            'password', 'password_confirm'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        # Par défaut, le compte est inactif jusqu'à la vérification OTP
        validated_data.pop('password_confirm')
        email = validated_data.get('email')
        password = validated_data.pop('password')

        # On utilise l'email comme username car Django (AbstractUser) nécessite un username unique
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_active=False,
            **validated_data
        )

        # Générer et enregistrer l'OTP
        otp_code = get_random_string(length=6, allowed_chars='0123456789')
        # L'OTP expire après 10 minutes
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        OTP.objects.create(user=user, code=otp_code, expires_at=expires_at)

        # TODO: Envoyer l'OTP par e-mail
        # send_mail(
        #     'Votre code de vérification CV_EXPRESS',
        #     f'Bonjour {user.username},\n\nVotre code de vérification est : {otp_code}\n\nCe code expirera dans 10 minutes.',
        #     'noreply@cvexpress.com',
        #     [user.email],
        #     fail_silently=False,
        # )
        print(f"DEBUG: OTP for {user.email}: {otp_code}") # À supprimer en production
        
        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile
    """
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'bio', 'phone', 'address',
            'date_of_birth', 'occupation', 'company', 'website',
            'linkedin', 'github'
        ]


class ProfileImageUploadSerializer(serializers.Serializer):
    """
    Serializer for profile image upload
    """
    profile_image = serializers.ImageField()

    def validate_profile_image(self, value):
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError('Image size must be less than 5MB.')
        
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
        ext = value.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError('Unsupported file extension.')
        
        return value


class OTPVerificationSerializer(serializers.Serializer):
    """
    Serializer pour la vérification du code OTP.
    """
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)


class OTPRequestSerializer(serializers.Serializer):
    """
    Serializer pour demander un nouveau code OTP.
    """
    email = serializers.EmailField()
