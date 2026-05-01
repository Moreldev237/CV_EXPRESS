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
]