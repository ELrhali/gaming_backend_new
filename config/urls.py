"""
URL configuration for gaming project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/admin-panel/dashboard/', permanent=False), name='home'),
    # Rediriger django-admin vers admin-panel
    path('django-admin/', RedirectView.as_view(url='/admin-panel/dashboard/', permanent=True)),
    path('django-admin/<path:path>', RedirectView.as_view(url='/admin-panel/dashboard/', permanent=True)),
    path('admin-panel/', include('admin_panel.urls')),
    path('api/', include('shop.urls')),  # API REST - Products
    path('api/', include('orders.urls')),  # API REST - Orders
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
