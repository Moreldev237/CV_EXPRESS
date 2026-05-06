from django.urls import path
from .views import (
    LandingView, AuthRegisterView, AuthVerifyOTPView, AuthLoginView,
    DashboardView, CVBuilderView, CVBuilderEditView, 
    SubscriptionView, ProfileView, current_user, health
)

app_name = 'frontend'

urlpatterns = [
    # Landing
    path('', LandingView.as_view(), name='landing'),
    
    # Auth
    path('auth/register/', AuthRegisterView.as_view(), name='register'),
    path('auth/verify-otp/', AuthVerifyOTPView.as_view(), name='verify-otp'),
    path('auth/login/', AuthLoginView.as_view(), name='login'),
    
    # Dashboard & Features
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('cv-builder/', CVBuilderView.as_view(), name='cv-builder'),
    path('cv-builder/<int:cv_id>/', CVBuilderEditView.as_view(), name='cv-builder-edit'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # API helpers
    path('api/user/', current_user, name='current-user'),
    path('health/', health, name='health'),
]
