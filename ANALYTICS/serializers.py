from rest_framework import serializers
from .models import UserActivity

class UserActivitySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'user_email', 'action', 'app_label', 'timestamp', 'extra_data']

class UsageStatsSerializer(serializers.Serializer):
    """Sérialiseur pour les statistiques globales du tableau de bord."""
    total_users = serializers.IntegerField()
    total_cvs = serializers.IntegerField()
    total_letters = serializers.IntegerField()
    total_activities = serializers.IntegerField()