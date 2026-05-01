from django.db import models
from django.conf import settings

class CoverLetterTemplate(models.Model):
    """Modèles visuels disponibles pour les lettres de motivation."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='cover_letter_templates/', null=True, blank=True)
    html_path = models.CharField(max_length=255, help_text="Chemin vers le fichier HTML du template")

    def __str__(self):
        return self.name

class CoverLetter(models.Model):
    """Contenu d'une lettre de motivation."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cover_letters')
    template = models.ForeignKey(CoverLetterTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, default="Ma lettre de motivation")
    
    # Informations destinataire
    recipient_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    recipient_address = models.TextField(blank=True)
    
    # Contenu
    subject = models.CharField(max_length=255)
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.email}"
