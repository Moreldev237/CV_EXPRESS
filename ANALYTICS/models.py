from django.db import models
from django.conf import settings

class UserActivity(models.Model):
    """Table de log pour l'activité des utilisateurs."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=255, help_text="Ex: CV_CREATED, PDF_EXPORTED, LOGIN")
    app_label = models.CharField(max_length=100, help_text="L'application concernée")
    timestamp = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(default=dict, blank=True, help_text="Données supplémentaires au format JSON")

    class Meta:
        verbose_name = "Activité Utilisateur"
        verbose_name_plural = "Activités Utilisateurs"
        ordering = ['-timestamp']

    def __str__(self):
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else 'N/A'
        return f"{self.user.email} - {self.action} - {timestamp_str}"