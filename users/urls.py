from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    ProfileView,
    UpdateProfileView,
    UploadProfileImageView,
    VerifyRegistrationOTPView,
    RequestNewOTPView,
)

urlpatterns = [
    # 🔐 Auth JWT
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 👤 User management
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/verify-otp/', VerifyRegistrationOTPView.as_view(), name='verify-otp'),
    path('auth/resend-otp/', RequestNewOTPView.as_view(), name='resend-otp'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),

    # 📸 Upload photo de profil
    path('profile/upload-image/', UploadProfileImageView.as_view(), name='upload-profile-image'),
]
