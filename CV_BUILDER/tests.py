from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date
from .models import CV, Template, Experience, Education, Skill, Language, Project

User = get_user_model()


class CVBuilderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="cv@example.com",
            username="cvuser",
            password="testpass123"
        )
        self.template = Template.objects.create(
            name="Modern Template",
            description="A modern CV template",
            html_path="templates/modern.html"
        )

    def test_cv_creation(self):
        cv = CV.objects.create(
            user=self.user,
            template=self.template,
            title="My Professional CV"
        )
        self.assertEqual(cv.user, self.user)
        self.assertEqual(cv.template, self.template)
        self.assertEqual(cv.title, "My Professional CV")
        self.assertEqual(str(cv), f"My Professional CV - {self.user.email}")

    def test_experience_creation(self):
        cv = CV.objects.create(user=self.user, title="Test CV")
        experience = Experience.objects.create(
            cv=cv,
            job_title="Software Developer",
            company="Tech Corp",
            location="Paris",
            start_date=date(2020, 1, 1),
            end_date=date(2023, 12, 31),
            description="Developed web applications"
        )
        self.assertEqual(experience.cv, cv)
        self.assertEqual(experience.job_title, "Software Developer")
        self.assertEqual(experience.company, "Tech Corp")

    def test_education_creation(self):
        cv = CV.objects.create(user=self.user, title="Test CV")
        education = Education.objects.create(
            cv=cv,
            degree="Master's in Computer Science",
            school="University of Paris",
            location="Paris",
            start_date=date(2016, 9, 1),
            end_date=date(2019, 6, 30),
            description="Specialized in AI and ML"
        )
        self.assertEqual(education.cv, cv)
        self.assertEqual(education.degree, "Master's in Computer Science")
        self.assertEqual(education.school, "University of Paris")

    def test_skill_creation(self):
        cv = CV.objects.create(user=self.user, title="Test CV")
        skill = Skill.objects.create(
            cv=cv,
            name="Python",
            level="expert"
        )
        self.assertEqual(skill.cv, cv)
        self.assertEqual(skill.name, "Python")
        self.assertEqual(skill.level, "expert")

    def test_language_creation(self):
        cv = CV.objects.create(user=self.user, title="Test CV")
        language = Language.objects.create(
            cv=cv,
            name="French",
            level="Maternel"
        )
        self.assertEqual(language.cv, cv)
        self.assertEqual(language.name, "French")
        self.assertEqual(language.level, "Maternel")

    def test_project_creation(self):
        cv = CV.objects.create(user=self.user, title="Test CV")
        project = Project.objects.create(
            cv=cv,
            title="E-commerce Platform",
            description="Built a full-stack e-commerce platform",
            link="https://github.com/example/project"
        )
        self.assertEqual(project.cv, cv)
        self.assertEqual(project.title, "E-commerce Platform")
        self.assertEqual(project.link, "https://github.com/example/project")
