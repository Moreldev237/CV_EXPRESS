from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CoverLetter, CoverLetterTemplate

User = get_user_model()


class CoverLetterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="letter@example.com",
            username="letteruser",
            password="testpass123"
        )
        self.template = CoverLetterTemplate.objects.create(
            name="Professional Template",
            description="A professional cover letter template",
            html_path="templates/professional.html"
        )

    def test_cover_letter_creation(self):
        cover_letter = CoverLetter.objects.create(
            user=self.user,
            template=self.template,
            title="Software Developer Application",
            content="Dear Hiring Manager,\n\nI am writing to apply for the Software Developer position..."
        )
        self.assertEqual(cover_letter.user, self.user)
        self.assertEqual(cover_letter.template, self.template)
        self.assertEqual(cover_letter.title, "Software Developer Application")
        self.assertIn("Dear Hiring Manager", cover_letter.content)

    def test_cover_letter_template_creation(self):
        template = CoverLetterTemplate.objects.create(
            name="Modern Template",
            description="A modern cover letter template",
            html_path="templates/modern.html"
        )
        self.assertEqual(template.name, "Modern Template")
        self.assertEqual(template.description, "A modern cover letter template")
        self.assertEqual(str(template), "Modern Template")
