from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def health_check(request):
    """Health check endpoint for monitoring and load balancers."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'ALX Travel App API',
    })


schema_view = get_schema_view(
    openapi.Info(
        title="ALX Travel App API",
        default_version='v1',
        description="API documentation for the ALX Travel App",
        contact=openapi.Contact(email="support@alxtravel.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', RedirectView.as_view(url='api/', permanent=False), name='home-redirect'),
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/', include('listings.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
