from django.urls import path
from .views import (

    # Lettres
    CoverLetterListCreateView,
    CoverLetterDetailView,

    # Génération automatique
    GenerateCoverLetterView,

    # Templates (modèles)
    CoverLetterTemplateListView,
    CoverLetterTemplateDetailView,

    # Export
    ExportCoverLetterPDFView,
)

urlpatterns = [

    # ==================== COVER LETTER ====================
    path('letters/', CoverLetterListCreateView.as_view(), name='letter-list-create'),
    path('letters/<int:pk>/', CoverLetterDetailView.as_view(), name='letter-detail'),
    path('letters/<int:pk>/export-pdf/', ExportCoverLetterPDFView.as_view(), name='letter-export-pdf'),

    # ==================== GENERATION AUTO ====================
    path('letters/generate/', GenerateCoverLetterView.as_view(), name='letter-generate'),

    # ==================== TEMPLATES ====================
    path('templates/', CoverLetterTemplateListView.as_view(), name='letter-template-list'),
    path('templates/<int:pk>/', CoverLetterTemplateDetailView.as_view(), name='letter-template-detail'),
]