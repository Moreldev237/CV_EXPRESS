from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="notification@example.com",
            username="notificationuser",
            password="testpass123"
        )

    def test_notification_creation(self):
        notification = Notification.objects.create(
            user=self.user,
            title="Welcome to CV Express",
            message="Thank you for joining our platform!",
            notification_type="SUCCESS"
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.title, "Welcome to CV Express")
        self.assertEqual(notification.message, "Thank you for joining our platform!")
        self.assertEqual(notification.notification_type, "SUCCESS")
        self.assertFalse(notification.is_read)
        self.assertIsNotNone(notification.created_at)

    def test_notification_str(self):
        notification = Notification.objects.create(
            user=self.user,
            title="Test Notification",
            message="This is a test"
        )
        expected_str = f"Test Notification - {self.user.email}"
        self.assertEqual(str(notification), expected_str)

    def test_notification_mark_as_read(self):
        notification = Notification.objects.create(
            user=self.user,
            title="Test",
            message="Test message"
        )
        self.assertFalse(notification.is_read)
        notification.is_read = True
        notification.save()
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
