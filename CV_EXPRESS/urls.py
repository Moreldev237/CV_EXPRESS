
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Schema view for Swagger/OpenAPI documentation
schema_view = get_schema_view(
    openapi.Info(
        title="API CV Express",
        default_version="v1",
        description="API pour l'application CV Express. Fournit des endpoints pour l'inscription, l'authentification (JWT), la gestion du profil et le téléchargement d'images.",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(name="Support API", email="support@cvexpress.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('CV_BUILDER.urls')),
    path('api/subscriptions/', include('SUBSCRIPTION.urls')),
    path('api/analytics/', include('ANALYTICS.urls')),
    path('api/notifications/', include('NOTIFICATIONS.urls')),
    
    # 🔗 Swagger / OpenAPI Documentation
    path('api/schema/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/schema/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/schema.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
