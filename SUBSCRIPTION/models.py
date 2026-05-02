from django.db import models
from django.conf import settings

class SubscriptionPlan(models.Model):
    """Définition des offres (ex: Free, Pro, Enterprise)."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField(default=1)
    features = models.JSONField(default=list, help_text="Liste des fonctionnalités incluses")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    """Lien entre un utilisateur et son abonnement actuel."""
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('canceled', 'Annulé'),
        ('expired', 'Expiré'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

class PaymentHistory(models.Model):
    """Journal des transactions effectuées."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.created_at})"
