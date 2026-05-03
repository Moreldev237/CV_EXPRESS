from django.db import models
from django.conf import settings
from django.utils import timezone


class SubscriptionPlan(models.Model):
    """Définition des offres (ex: Free, Pro, Enterprise)."""
    BILLING_INTERVAL_CHOICES = [
        ('month', 'Mensuel'),
        ('year', 'Annuel'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField(default=1)
    interval = models.CharField(max_length=10, choices=BILLING_INTERVAL_CHOICES, default='month')
    features = models.JSONField(default=list, help_text="Liste des fonctionnalités incluses")
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ID du prix Stripe. Permet de gérer le paiement récurrent via Stripe Checkout."
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage pour les plans, du plus populaire au plus avancé.")

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return self.name

    @property
    def is_free(self):
        return self.price == 0

    @property
    def interval_display(self):
        return dict(self.BILLING_INTERVAL_CHOICES).get(self.interval, self.interval)


class UserSubscription(models.Model):
    """Lien entre un utilisateur et son abonnement actuel."""
    STATUS_CHOICES = [
        ('pending', 'En attente de paiement'),
        ('active', 'Actif'),
        ('canceled', 'Annulé'),
        ('expired', 'Expiré'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

    @property
    def is_active(self):
        return self.status == 'active' and self.end_date > timezone.now()

    @property
    def remaining_days(self):
        return max((self.end_date - timezone.now()).days, 0)


class PaymentHistory(models.Model):
    """Journal des transactions effectuées."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.created_at})"
