from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import OTP

User = get_user_model()


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123",
            bio="Test bio",
            phone="+1234567890",
            address="123 Test St",
            occupation="Developer",
            company="Test Corp"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertEqual(self.user.bio, "Test bio")
        self.assertEqual(self.user.phone, "+1234567890")

    def test_is_premium_property(self):
        # Test user without subscription
        self.assertFalse(self.user.is_premium)

        # Create a subscription plan and subscription
        from SUBSCRIPTION.models import SubscriptionPlan, UserSubscription
        plan = SubscriptionPlan.objects.create(
            name="Pro",
            description="Pro plan",
            price=9.99,
            duration_months=1
        )
        subscription = UserSubscription.objects.create(
            user=self.user,
            plan=plan,
            status='active',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
        self.assertTrue(self.user.is_premium)

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "test@example.com")


class OTPModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="otp@example.com",
            username="otpuser",
            password="testpass123"
        )
        self.otp = OTP.objects.create(
            user=self.user,
            code="123456",
            expires_at=timezone.now() + timedelta(minutes=5)
        )

    def test_otp_creation(self):
        self.assertEqual(self.otp.user, self.user)
        self.assertEqual(self.otp.code, "123456")
        self.assertFalse(self.otp.is_verified)
        self.assertFalse(self.otp.is_expired)

    def test_otp_expiration(self):
        expired_otp = OTP.objects.create(
            user=self.user,
            code="654321",
            expires_at=timezone.now() - timedelta(minutes=1)
        )
        self.assertTrue(expired_otp.is_expired)

    def test_otp_str_method(self):
        self.assertEqual(str(self.otp), f"OTP pour {self.user.email}")
