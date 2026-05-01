from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


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
