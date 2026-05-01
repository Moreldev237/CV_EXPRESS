
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
        title="CV Express API",
        default_version="v1",
        description="API for CV Express application. Provides endpoints for user registration, authentication (JWT), profile management, and profile image uploads.",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(name="API Support", email="support@cvexpress.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    
    # 🔗 Swagger / OpenAPI Documentation
    path('api/schema/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/schema/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/schema.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
