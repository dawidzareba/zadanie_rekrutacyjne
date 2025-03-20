from django.urls import path
from .views import ShortenUrlView, ExpandUrlView, redirect_view

urlpatterns = [
    path('api/shorten/', ShortenUrlView.as_view(), name='shorten_url'),
    path('api/expand/<str:short_code>/', ExpandUrlView.as_view(), name='expand_url'),
    path('r/<str:short_code>/', redirect_view, name='redirect_url'),
]