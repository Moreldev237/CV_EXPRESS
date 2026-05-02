from .models import Notification
from .tasks import send_email_notification_task, send_push_notification_task

def notify_user(user, title, message, notification_type='INFO', email=False, push=False):
    """
    Déclenche une notification multi-canal de manière asynchrone.
    """
    # 1. Création de l'alerte in-app (Persistance)
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )

    # 2. Envoi de l'email asynchrone (via Celery)
    if email and user.email:
        send_email_notification_task.delay(title, message, [user.email])

    # 3. Envoi de la notification push asynchrone (via Celery)
    if push:
        send_push_notification_task.delay(user.id, title, message)