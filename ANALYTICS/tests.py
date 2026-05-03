from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import UserActivity

User = get_user_model()


class AnalyticsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="analytics@example.com",
            username="analyticsuser",
            password="testpass123"
        )

    def test_user_activity_creation(self):
        activity = UserActivity.objects.create(
            user=self.user,
            action="CV_CREATED",
            app_label="CV_BUILDER",
            extra_data={"cv_id": 1, "template": "modern"}
        )
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.action, "CV_CREATED")
        self.assertEqual(activity.app_label, "CV_BUILDER")
        self.assertEqual(activity.extra_data["cv_id"], 1)
        self.assertIsNotNone(activity.timestamp)

    def test_user_activity_str(self):
        activity = UserActivity.objects.create(
            user=self.user,
            action="LOGIN",
            app_label="users"
        )
        expected_str = f"{self.user.email} - LOGIN - {activity.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        self.assertEqual(str(activity), expected_str)
