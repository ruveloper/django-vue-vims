from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    # * Project URLs
    # API base url
    path("api/", include("apps.api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
