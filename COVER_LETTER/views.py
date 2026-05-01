from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CoverLetter, CoverLetterTemplate
from .serializers import CoverLetterSerializer, CoverLetterTemplateSerializer

class CoverLetterListCreateView(generics.ListCreateAPIView):
    """Liste et création de lettres de motivation."""
    serializer_class = CoverLetterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)

    @swagger_auto_schema(tags=['Cover Letter'], operation_summary="Lister les lettres de motivation")
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cover Letter'], operation_summary="Lister ou créer des lettres")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CoverLetterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Détail, modification et suppression d'une lettre."""
    serializer_class = CoverLetterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)

    @swagger_auto_schema(tags=['Cover Letter'], operation_summary="Gérer une lettre spécifique")
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cover Letter'], operation_summary="Mettre à jour une lettre")
    def put(self, request, *args, **kwargs): return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cover Letter'], operation_summary="Mise à jour partielle d'une lettre")
    def patch(self, request, *args, **kwargs): return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cover Letter'], operation_summary="Supprimer une lettre")
    def delete(self, request, *args, **kwargs): return super().delete(request, *args, **kwargs)

class CoverLetterTemplateListView(generics.ListAPIView):
    """Liste des modèles visuels pour lettres."""
    queryset = CoverLetterTemplate.objects.all()
    serializer_class = CoverLetterTemplateSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=['Cover Letter Templates'], operation_summary="Lister les templates de lettres")
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

class CoverLetterTemplateDetailView(generics.RetrieveAPIView):
    """Détail d'un modèle visuel spécifique."""
    queryset = CoverLetterTemplate.objects.all()
    serializer_class = CoverLetterTemplateSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=['Cover Letter Templates'], operation_summary="Détails d'un template de lettre")
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

class GenerateCoverLetterView(APIView):
    """
    Endpoint pour la génération automatique via IA.
    Fera le pont avec l'application AI_ASSISTANT.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Cover Letter'],
        operation_summary="Générer automatiquement une lettre (IA)",
        operation_description="Utilise l'IA pour rédiger le contenu basé sur un CV ou une offre d'emploi.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'cv_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID du CV à utiliser'),
                'job_description': openapi.Schema(type=openapi.TYPE_STRING, description='Description du poste'),
            }
        )
    )
    def post(self, request):
        # Cette logique sera connectée à l'IA plus tard
        return Response({
            "message": "Fonctionnalité de génération IA en cours de développement.",
            "suggested_content": "Cher [Nom], Je postule avec enthousiasme..."
        }, status=status.HTTP_200_OK)

class ExportCoverLetterPDFView(APIView):
    """
    Endpoint pour l'exportation de la lettre de motivation en PDF.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Cover Letter'], 
        operation_summary="Exporter la lettre en PDF",
        responses={200: openapi.Response("Fichier PDF de la lettre")}
    )
    def get(self, request, pk):
        letter = get_object_or_404(CoverLetter, pk=pk, user=request.user)
        
        # 1. Sérialiser les données de la lettre
        serializer = CoverLetterSerializer(letter)
        data = serializer.data

        # 2. Déterminer le chemin du template HTML
        template_path = letter.template.html_path if letter.template else 'cover_letter_templates/default.html'

        # 3. Générer le HTML
        html_string = render_to_string(template_path, {
            'letter': data,
            'user': request.user
        })

        # 4. Conversion HTML -> PDF
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

        # 5. Réponse de téléchargement
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="lettre_{letter.id}.pdf"'
        
        return response
