from rest_framework import generics, permissions, views
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import UserActivity
from .serializers import UserActivitySerializer, UsageStatsSerializer
from CV_BUILDER.models import CV
from COVER_LETTER.models import CoverLetter
from users.models import User

class UserActivityListView(generics.ListAPIView):
    """Récupère l'historique complet des activités (Admin uniquement)."""
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return UserActivity.objects.all()

    @swagger_auto_schema(
        tags=['Analytics'],
        operation_summary="Lister toutes les activités utilisateurs"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class DashboardStatsView(views.APIView):
    """Fournit des statistiques agrégées pour le tableau de bord administrateur."""
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        tags=['Analytics'],
        operation_summary="Statistiques globales d'utilisation",
        responses={200: UsageStatsSerializer}
    )
    def get(self, request):
        data = {
            'total_users': User.objects.count(),
            'total_cvs': CV.objects.count(),
            'total_letters': CoverLetter.objects.count(),
            'total_activities': UserActivity.objects.count()
        }
        serializer = UsageStatsSerializer(data)
        return Response(serializer.data)