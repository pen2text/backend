
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Pen2Text API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="capstone@durye.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_management.urls')),
    path('api/', include('authentication.urls')),
    path('api/', include('package_manager.urls')),
    path('api/', include('converter.urls')),
    path('api/', include('admin_config.urls')),
    path('api/', include('admin_dashboard.urls')),
    path('api/', include('chapa_gateway.urls')),
    path('api/', include('remote_handler.urls')),
    path('api/', include('conversion_management.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
