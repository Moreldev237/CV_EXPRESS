from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds profile image field and additional user information.
    """
    email = models.EmailField(_('email address'), unique=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        default='default_profile.png'
    )
    bio = models.TextField(max_length=500, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    date_of_birth = models.DateField(null=True, blank=True)
    
    # CV related fields
    occupation = models.CharField(max_length=100, blank=True, default='')
    company = models.CharField(max_length=100, blank=True, default='')
    website = models.URLField(blank=True, default='')
    linkedin = models.URLField(blank=True, default='')
    github = models.URLField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def is_premium(self):
        subscription = getattr(self, 'subscription', None)
        return bool(
            subscription
            and subscription.status == 'active'
            and subscription.end_date > timezone.now()
            and not subscription.plan.is_free
        )


class OTP(models.Model):
    """
    Modèle pour stocker les codes OTP (One-Time Password) pour la vérification de l'utilisateur.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('OTP')
        verbose_name_plural = _('OTPs')
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP pour {self.user.email}"

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at
