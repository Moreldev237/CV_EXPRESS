from django.urls import path
from .views import (

    # CV
    CVListCreateView,
    CVDetailView,

    # Templates (modèles de CV)
    TemplateListView,
    TemplateDetailView,

    # Export PDF
    ExportCVPDFView,

    # Option bonus
    CVFullDetailView,

    # Sections du CV
    ExperienceListCreateView,
    ExperienceDetailView,
    EducationListCreateView,
    EducationDetailView,
    SkillListCreateView,
    SkillDetailView,
    LanguageListCreateView,
    LanguageDetailView,
    ProjectListCreateView,
    ProjectDetailView,
)

urlpatterns = [

    # ==================== CV ====================
    path('cvs/', CVListCreateView.as_view(), name='cv-list-create'),
    path('cvs/<int:pk>/', CVDetailView.as_view(), name='cv-detail'),

    # 🔥 récupérer tout le CV avec ses sections
    path('cvs/<int:pk>/full/', CVFullDetailView.as_view(), name='cv-full-detail'),

    # ==================== TEMPLATES ====================
    path('templates/', TemplateListView.as_view(), name='template-list'),
    path('templates/<int:pk>/', TemplateDetailView.as_view(), name='template-detail'),

    # ==================== EXPORT PDF ====================
    path('cvs/<int:pk>/export-pdf/', ExportCVPDFView.as_view(), name='cv-export-pdf'),

    # ==================== SECTIONS DU CV ====================
    path('cvs/<int:cv_id>/experiences/', ExperienceListCreateView.as_view(), name='experience-list-create'),
    path('experiences/<int:pk>/', ExperienceDetailView.as_view(), name='experience-detail'),

    path('cvs/<int:cv_id>/educations/', EducationListCreateView.as_view(), name='education-list-create'),
    path('educations/<int:pk>/', EducationDetailView.as_view(), name='education-detail'),

    path('cvs/<int:cv_id>/skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),

    path('cvs/<int:cv_id>/languages/', LanguageListCreateView.as_view(), name='language-list-create'),
    path('languages/<int:pk>/', LanguageDetailView.as_view(), name='language-detail'),

    path('cvs/<int:cv_id>/projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]