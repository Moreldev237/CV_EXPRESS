from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from drf_yasg.utils import swagger_auto_schema
from .models import CV, Template
from .serializers import CVSerializer, CVFullSerializer, TemplateSerializer

class CVListCreateView(generics.ListCreateAPIView):
    """Liste et création de CV pour l'utilisateur connecté."""
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['CV Builder'], operation_summary="Lister les CV de l'utilisateur")
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['CV Builder'], operation_summary="Créer un nouveau CV")
    def post(self, request, *args, **kwargs): return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)

class CVDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Détails, modification et suppression d'un CV."""
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['CV Builder'], operation_summary="Détails d'un CV")
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)
    @swagger_auto_schema(tags=['CV Builder'], operation_summary="Mettre à jour un CV")
    def put(self, request, *args, **kwargs): return super().put(request, *args, **kwargs)
    @swagger_auto_schema(tags=['CV Builder'], operation_summary="Supprimer un CV")
    def delete(self, request, *args, **kwargs): return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)

class CVFullDetailView(generics.RetrieveAPIView):
    """Récupère un CV avec toutes ses sections (expériences, formations, etc.)."""
    serializer_class = CVFullSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['CV Builder'], 
        operation_summary="Récupérer le CV complet",
        operation_description="Récupère le CV avec toutes les sections (Expériences, Études, Compétences, etc.) imbriquées."
    )
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)

class TemplateListView(generics.ListAPIView):
    """Liste des templates disponibles (accessible à tous)."""
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=['Templates'], operation_summary="Lister les modèles de CV")
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

class TemplateDetailView(generics.RetrieveAPIView):
    """Détail d'un template spécifique."""
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        tags=['Templates'],
        operation_summary="Détails d'un modèle visuel",
        operation_description="Récupère les informations d'un template spécifique (nom, aperçu, chemin HTML)."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ExportCVPDFView(APIView):
    """
    Endpoint pour l'exportation PDF.
    Note: Nécessite l'intégration d'une librairie comme WeasyPrint.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['Export'], operation_summary="Générer le CV en format PDF")
    def get(self, request, pk):
        cv = get_object_or_404(CV, pk=pk, user=request.user)
        
        # 1. Récupérer les données complètes (imbriquées) du CV
        serializer = CVFullSerializer(cv)
        cv_data = serializer.data

        # 2. Déterminer le chemin du template HTML (ou un par défaut)
        template_path = cv.template.html_path if cv.template else 'cv_templates/default.html'

        # 3. Générer le contenu HTML à partir du template Django
        html_string = render_to_string(template_path, {
            'cv': cv_data,
            'user': request.user
        })

        # 4. Conversion HTML -> PDF via WeasyPrint
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

        # 5. Préparation de la réponse HTTP pour le téléchargement
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="cv_{cv.id}.pdf"'
        
        return response
