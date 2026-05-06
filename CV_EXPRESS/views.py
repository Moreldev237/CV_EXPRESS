from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
import json

# Frontend Template Views (public - client-side auth)
class LandingView(TemplateView):
    template_name = 'index.html'
    
class AuthRegisterView(TemplateView):
    template_name = 'auth/register.html'

class AuthVerifyOTPView(TemplateView):
    template_name = 'auth/verify-otp.html'

class AuthLoginView(TemplateView):
    template_name = 'auth/login.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class CVBuilderView(TemplateView):
    template_name = 'cv-builder.html'

class CVBuilderEditView(TemplateView):
    template_name = 'cv-builder.html'  # Same template with cv_id param

class SubscriptionView(TemplateView):
    template_name = 'subscription.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

# API endpoint for current user profile (for frontend)
@api_view(['GET'])
@permission_classes([AllowAny])
def current_user(request):
    """Returns current user info or null if not authenticated"""
    if request.user.is_authenticated:
        from users.serializers import UserSerializer
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response(None)

# Health check
def health(request):
    return JsonResponse({'status': 'ok', 'frontend': 'ready'})
