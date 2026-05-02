from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from .models import SubscriptionPlan, UserSubscription, PaymentHistory
from .serializers import (
    SubscriptionPlanSerializer, UserSubscriptionSerializer, 
    PaymentHistorySerializer, SubscribeRequestSerializer
)

class SubscriptionPlanListView(generics.ListAPIView):
    """Liste des plans d'abonnement disponibles."""
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=['Subscription - Plans'])
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

class SubscriptionPlanDetailView(generics.RetrieveAPIView):
    """Détails d'un plan spécifique."""
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=['Subscription - Plans'])
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

class UserSubscriptionView(generics.RetrieveAPIView):
    """Récupère l'abonnement actif de l'utilisateur connecté."""
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['Subscription - User'])
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

    def get_object(self):
        # Protection pour Swagger lors de la génération du schéma
        if getattr(self, 'swagger_fake_view', False):
            return None
        return get_object_or_404(UserSubscription, user=self.request.user)

class SubscribeView(APIView):
    """Endpoint pour souscrire à un plan."""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Subscription - User'],
        request_body=SubscribeRequestSerializer,
        responses={201: UserSubscriptionSerializer()}
    )
    def post(self, request):
        # Logique simplifiée : En production, connecter ici Stripe/PayPal
        return Response({"message": "Redirection vers le paiement ou activation du plan."}, status=status.HTTP_201_CREATED)

class CancelSubscriptionView(APIView):
    """Annule l'abonnement automatique."""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Subscription - User'],
        operation_summary="Résilier l'abonnement",
        responses={200: openapi.Response("Abonnement annulé")}
    )
    def post(self, request):
        sub = get_object_or_404(UserSubscription, user=request.user)
        sub.status = 'canceled'
        sub.save()
        return Response({"message": "Abonnement annulé avec succès."})

class UpgradeSubscriptionView(APIView):
    @swagger_auto_schema(
        tags=['Subscription - User'], 
        operation_summary="Passer à un plan supérieur",
        request_body=SubscribeRequestSerializer
    )
    def post(self, request): return Response({"message": "Upgrade en cours..."})

class DowngradeSubscriptionView(APIView):
    @swagger_auto_schema(
        tags=['Subscription - User'], 
        operation_summary="Passer à un plan inférieur",
        request_body=SubscribeRequestSerializer
    )
    def post(self, request): return Response({"message": "Downgrade programmé..."})

class CreatePaymentIntentView(APIView):
    """Initialise une intention de paiement."""
    @swagger_auto_schema(
        tags=['Subscription - Payment'],
        operation_summary="Créer une intention de paiement (Stripe)",
        request_body=SubscribeRequestSerializer
    )
    def post(self, request):
        return Response({"client_secret": "pi_mock_secret_123", "publishable_key": "pk_test_mock"})

class PaymentSuccessView(APIView):
    """Webhook ou redirect après succès du paiement."""
    @swagger_auto_schema(
        tags=['Subscription - Payment'],
        operation_summary="Confirmation de succès",
        manual_parameters=[
            openapi.Parameter('session_id', openapi.IN_QUERY, description="ID de session Stripe", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        return Response({"message": "Paiement validé ! Votre compte est maintenant premium."})

class PaymentCancelView(APIView):
    """Redirect après abandon du paiement."""
    @swagger_auto_schema(tags=['Subscription - Payment'])
    def get(self, request):
        return Response({"message": "Paiement annulé."})

class SubscriptionHistoryView(generics.ListAPIView):
    """Historique des factures et paiements."""
    serializer_class = PaymentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return PaymentHistory.objects.none()
        return PaymentHistory.objects.filter(user=self.request.user)

    @swagger_auto_schema(tags=['Subscription - History'])
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)
