from django.urls import path
from .views import (

    # Plans d'abonnement
    SubscriptionPlanListView,
    SubscriptionPlanDetailView,

    # Abonnement utilisateur
    UserSubscriptionView,
    SubscribeView,
    CancelSubscriptionView,
    UpgradeSubscriptionView,
    DowngradeSubscriptionView,

    # Paiement
    CreatePaymentIntentView,
    PaymentSuccessView,
    PaymentCancelView,

    # Historique
    SubscriptionHistoryView,
)

urlpatterns = [

    # ==================== PLANS ====================
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plan-list'),
    path('plans/<int:pk>/', SubscriptionPlanDetailView.as_view(), name='subscription-plan-detail'),

    # ==================== USER SUBSCRIPTION ====================
    path('me/', UserSubscriptionView.as_view(), name='user-subscription'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel-subscription'),
    path('upgrade/', UpgradeSubscriptionView.as_view(), name='upgrade-subscription'),
    path('downgrade/', DowngradeSubscriptionView.as_view(), name='downgrade-subscription'),

    # ==================== PAYMENT ====================
    path('payment/create/', CreatePaymentIntentView.as_view(), name='create-payment'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('payment/cancel/', PaymentCancelView.as_view(), name='payment-cancel'),

    # ==================== HISTORY ====================
    path('history/', SubscriptionHistoryView.as_view(), name='subscription-history'),
]