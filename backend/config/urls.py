from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from apps.common.routers import OptionalSlashRouter
from apps.url_shortener.views import UrlViewSet
from apps.url_shortener.models import Url

router = OptionalSlashRouter()
router.register('urls', UrlViewSet, basename='urls')


def get_original_url(request, short_code):
    url_obj = get_object_or_404(Url, short_code=short_code)
    return JsonResponse({'original_url': url_obj.original_url})

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/url/<str:short_code>', get_original_url, name='get_original_url'),
]
