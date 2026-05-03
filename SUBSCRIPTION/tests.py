from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, UserSubscription, PaymentHistory

User = get_user_model()


class SubscriptionPlanTestCase(TestCase):
    def setUp(self):
        self.free_plan = SubscriptionPlan.objects.create(
            name="Free",
            description="Plan gratuit",
            price=0,
            duration_months=1,
            features=["CV basique", "1 export"]
        )
        self.pro_plan = SubscriptionPlan.objects.create(
            name="Pro",
            description="Plan professionnel",
            price=9.99,
            duration_months=1,
            features=["CV avancé", "Exports illimités", "IA"]
        )

    def test_is_free_property(self):
        self.assertTrue(self.free_plan.is_free)
        self.assertFalse(self.pro_plan.is_free)

    def test_interval_display(self):
        self.assertEqual(self.free_plan.interval_display, 'Mensuel')
        self.assertEqual(self.pro_plan.interval_display, 'Mensuel')


class UserSubscriptionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        self.plan = SubscriptionPlan.objects.create(
            name="Test Plan",
            description="Plan de test",
            price=5.99,
            duration_months=1
        )

    def test_subscription_creation(self):
        subscription = UserSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            status='active',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertTrue(subscription.is_active)

    def test_remaining_days(self):
        future_date = timezone.now() + timedelta(days=10)
        subscription = UserSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            status='active',
            start_date=timezone.now(),
            end_date=future_date
        )
        # Allow for small timing differences (should be 9 or 10)
        self.assertIn(subscription.remaining_days, [9, 10])


class PaymentHistoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="payment@example.com",
            username="paymentuser",
            password="testpass123"
        )

    def test_payment_creation(self):
        payment = PaymentHistory.objects.create(
            user=self.user,
            amount=9.99,
            status="paid",
            transaction_id="txn_123456",
            description="Abonnement Pro"
        )
        self.assertEqual(payment.user, self.user)
        self.assertEqual(float(payment.amount), 9.99)
        self.assertEqual(payment.status, "paid")
