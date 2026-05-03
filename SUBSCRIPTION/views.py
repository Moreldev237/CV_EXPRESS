import stripe
from datetime import timedelta
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import SubscriptionPlan, UserSubscription, PaymentHistory
from .serializers import (
    SubscriptionPlanSerializer, UserSubscriptionSerializer,
    PaymentHistorySerializer, SubscribeRequestSerializer
)

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionPlanListView(generics.ListAPIView):
    """Liste des plans d'abonnement disponibles."""
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=['Subscription - Plans'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubscriptionPlanDetailView(generics.RetrieveAPIView):
    """Détails d'un plan spécifique."""
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=['Subscription - Plans'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserSubscriptionView(generics.RetrieveAPIView):
    """Récupère l'abonnement actif de l'utilisateur connecté."""
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['Subscription - User'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
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
        serializer = SubscribeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = get_object_or_404(SubscriptionPlan, id=serializer.validated_data['plan_id'], is_active=True)
        user = request.user

        if plan.is_free:
            end_date = timezone.now() + timedelta(days=30 * plan.duration_months)
            subscription, _ = UserSubscription.objects.update_or_create(
                user=user,
                defaults={
                    'plan': plan,
                    'status': 'active',
                    'start_date': timezone.now(),
                    'end_date': end_date,
                    'stripe_subscription_id': None,
                    'stripe_customer_id': None,
                }
            )
            return Response(UserSubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)

        if not settings.STRIPE_SECRET_KEY:
            return Response({"detail": "Stripe n'est pas configuré."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if plan.stripe_price_id:
            line_items = [{'price': plan.stripe_price_id, 'quantity': 1}]
        else:
            line_items = [{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': plan.name,
                        'description': plan.description,
                    },
                    'unit_amount': int(plan.price * 100),
                    'recurring': {
                        'interval': plan.interval,
                    },
                },
                'quantity': 1,
            }]

        success_url = request.build_absolute_uri('/api/subscriptions/payment/success/?session_id={CHECKOUT_SESSION_ID}')
        cancel_url = request.build_absolute_uri('/api/subscriptions/payment/cancel/')

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='subscription',
            customer_email=user.email,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={'user_id': str(user.id), 'plan_id': str(plan.id)},
        )

        UserSubscription.objects.update_or_create(
            user=user,
            defaults={
                'plan': plan,
                'status': 'pending',
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=30 * plan.duration_months),
                'stripe_subscription_id': None,
                'stripe_customer_id': session.customer,
            }
        )

        return Response({
            'checkout_url': session.url,
            'session_id': session.id,
        }, status=status.HTTP_201_CREATED)


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
        sub.end_date = timezone.now()
        sub.save()
        return Response({"message": "Abonnement annulé avec succès."})


class UpgradeSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Subscription - User'],
        operation_summary="Passer à un plan supérieur",
        request_body=SubscribeRequestSerializer
    )
    def post(self, request):
        current = get_object_or_404(UserSubscription, user=request.user)
        serializer = SubscribeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = get_object_or_404(SubscriptionPlan, id=serializer.validated_data['plan_id'], is_active=True)
        if plan.price <= current.plan.price:
            return Response({"detail": "Veuillez sélectionner un plan supérieur."}, status=status.HTTP_400_BAD_REQUEST)

        request.data['plan_id'] = plan.id
        return SubscribeView().post(request)


class DowngradeSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Subscription - User'],
        operation_summary="Passer à un plan inférieur",
        request_body=SubscribeRequestSerializer
    )
    def post(self, request):
        current = get_object_or_404(UserSubscription, user=request.user)
        serializer = SubscribeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = get_object_or_404(SubscriptionPlan, id=serializer.validated_data['plan_id'], is_active=True)
        if plan.price >= current.plan.price:
            return Response({"detail": "Veuillez sélectionner un plan inférieur."}, status=status.HTTP_400_BAD_REQUEST)

        current.plan = plan
        current.status = 'active'
        current.end_date = timezone.now() + timedelta(days=30 * plan.duration_months)
        current.save()
        return Response(UserSubscriptionSerializer(current).data)


class CreatePaymentIntentView(APIView):
    """Initialise une intention de paiement."""
    @swagger_auto_schema(
        tags=['Subscription - Payment'],
        operation_summary="Créer une intention de paiement (Stripe)",
        request_body=SubscribeRequestSerializer
    )
    def post(self, request):
        serializer = SubscribeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = get_object_or_404(SubscriptionPlan, id=serializer.validated_data['plan_id'], is_active=True)
        if plan.is_free:
            return Response({"detail": "Ce plan est gratuit, aucun paiement requis."}, status=status.HTTP_400_BAD_REQUEST)

        if not settings.STRIPE_SECRET_KEY:
            return Response({"detail": "Stripe n'est pas configuré."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        intent = stripe.PaymentIntent.create(
            amount=int(plan.price * 100),
            currency='usd',
            metadata={'user_id': str(request.user.id), 'plan_id': str(plan.id)},
        )
        return Response({
            'client_secret': intent.client_secret,
            'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        })


class PaymentSuccessView(APIView):
    """Redirect après succès du paiement."""
    @swagger_auto_schema(
        tags=['Subscription - Payment'],
        operation_summary="Confirmation de succès",
        manual_parameters=[
            openapi.Parameter('session_id', openapi.IN_QUERY, description="ID de session Stripe", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response({"detail": "Session Stripe manquante."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(session_id, expand=['subscription', 'customer'])
        except stripe.error.StripeError:
            return Response({"detail": "Impossible de récupérer la session Stripe."}, status=status.HTTP_400_BAD_REQUEST)

        plan_id = session.metadata.get('plan_id')
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        user = request.user

        subscription = get_object_or_404(UserSubscription, user=user)
        subscription.status = 'active'
        subscription.stripe_subscription_id = session.subscription
        subscription.stripe_customer_id = session.customer
        subscription.save()

        PaymentHistory.objects.get_or_create(
            user=user,
            transaction_id=session.payment_intent,
            defaults={
                'amount': plan.price,
                'status': 'paid',
                'description': f'Abonnement {plan.name}',
            }
        )

        return Response({"message": "Paiement validé ! Votre compte est maintenant premium."})


class PaymentCancelView(APIView):
    """Redirect après abandon du paiement."""
    @swagger_auto_schema(tags=['Subscription - Payment'])
    def get(self, request):
        return Response({"message": "Paiement annulé."})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)

        if not webhook_secret:
            return Response({"detail": "Stripe webhook secret not configuré."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            self._handle_checkout_session(session)

        return Response(status=status.HTTP_200_OK)

    def _handle_checkout_session(self, session):
        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')
        plan_id = metadata.get('plan_id')
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except (User.DoesNotExist, SubscriptionPlan.DoesNotExist):
            return

        start_date = timezone.now()
        end_date = start_date + timedelta(days=30 * plan.duration_months)

        subscription, _ = UserSubscription.objects.update_or_create(
            user=user,
            defaults={
                'plan': plan,
                'status': 'active',
                'start_date': start_date,
                'end_date': end_date,
                'stripe_subscription_id': session.get('subscription'),
                'stripe_customer_id': session.get('customer'),
            }
        )

        PaymentHistory.objects.get_or_create(
            user=user,
            transaction_id=session.get('payment_intent') or session.get('id'),
            defaults={
                'amount': plan.price,
                'status': 'paid',
                'description': f'Abonnement {plan.name}',
            }
        )


class SubscriptionHistoryView(generics.ListAPIView):
    """Historique des factures et paiements."""
    serializer_class = PaymentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return PaymentHistory.objects.none()
        return PaymentHistory.objects.filter(user=self.request.user)

    @swagger_auto_schema(tags=['Subscription - History'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
