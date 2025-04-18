from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .models import ShortUrl
from .serializers import UrlSerializer, UrlCreateSerializer


class UrlViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = ShortUrl.objects.all()
    lookup_field = "short_code"

    throttle_classes = [ScopedRateThrottle]
    throttle_scope_map = {
        "create": "url_create",
        "retrieve": "url_retrieve",
    }

    def get_throttles(self):
        if self.action in self.throttle_scope_map:
            self.throttle_scope = self.throttle_scope_map[self.action]

        return super().get_throttles()

    def get_serializer_class(self):
        if self.action == self.create.__name__:
            return UrlCreateSerializer

        return UrlSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        response_serializer = UrlSerializer(instance, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(60 * 60 * 24))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
