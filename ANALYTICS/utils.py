from .models import UserActivity

def log_activity(user, action, app_label, extra_data=None, request=None):
    """
    Enregistre une activité utilisateur dans la base de données.
    """
    if extra_data is None:
        extra_data = {}

    if request:
        extra_data['ip'] = request.META.get('REMOTE_ADDR')
        extra_data['user_agent'] = request.META.get('HTTP_USER_AGENT')

    return UserActivity.objects.create(
        user=user,
        action=action,
        app_label=app_label,
        extra_data=extra_data
    )