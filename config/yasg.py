from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework import permissions


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Documentation API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser]
)

urlpatterns = [
    path('api_docs/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger"),
]