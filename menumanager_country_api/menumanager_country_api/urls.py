from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from base_app.admin_base import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('v1/menus/', include('menus.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
