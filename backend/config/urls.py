from django.contrib import admin
from django.urls import path, include

from apps.common.routers import OptionalSlashRouter
from apps.url_shortener.views import UrlViewSet

router = OptionalSlashRouter()
router.register('urls', UrlViewSet, basename='urls')


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
]
