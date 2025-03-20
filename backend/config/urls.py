from django.contrib import admin
from django.urls import path, include

router = OptionalSlashRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
]
