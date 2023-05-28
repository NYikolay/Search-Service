from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('search_service.urls', namespace='search_service')),
    path('health-check-status/', lambda x: HttpResponse(), name='health_check_status'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('__debug__/', include('debug_toolbar.urls')),
]
