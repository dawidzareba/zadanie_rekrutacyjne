from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from apps.common.routers import OptionalSlashRouter
from apps.urls.views import UrlViewSet

router = OptionalSlashRouter()
router.register("urls", UrlViewSet, basename="urls")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

if settings.SILK_ENABLED:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
