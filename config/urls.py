# config/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Ayurvedic Hospital API",
        default_version='v1',
        description="API documentation for the AI-powered Ayurvedic hospital backend.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@ayurvedichospital.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('secure-admin-2025/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/prana-ai/', include('prana_ai.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/core/', include('core.urls')),
]


urlpatterns += [
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
