from django.urls import path
from .views import UserActivityListView, DashboardStatsView

urlpatterns = [
    path('activities/', UserActivityListView.as_view(), name='user-activity-list'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]