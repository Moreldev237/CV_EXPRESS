from django.utils import timezone
from rest_framework.permissions import BasePermission


class IsPremiumUser(BasePermission):
    message = "Cette fonctionnalité est réservée aux abonnés premium."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        subscription = getattr(user, 'subscription', None)
        return bool(
            subscription
            and subscription.status == 'active'
            and subscription.end_date > timezone.now()
            and not subscription.plan.is_free
        )
