from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

@shared_task
def send_email_notification_task(subject, message, recipient_list):
    """Tâche asynchrone pour l'envoi d'emails."""
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=True,
    )

@shared_task
def send_push_notification_task(user_id, title, message, data=None):
    """
    Tâche asynchrone pour l'envoi de notifications push.
    Prêt pour l'intégration avec django-fcm.
    """
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        # Simulation de l'envoi (Ici on utiliserait FCMDevice.send_message)
        print(f"DEBUG: Push envoyé à {user.email}: {title}")
        return True
    except User.DoesNotExist:
        return False