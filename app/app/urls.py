from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import debug
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Default django site - just to see something at app start.
    path("", debug.default_urlconf),
    path("admin/", admin.site.urls),
    # API docs endpoints
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="api-schema"
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    # All images.urls endpoints included
    path("api/images/", include("images.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
