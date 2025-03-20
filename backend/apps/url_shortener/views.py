from django.shortcuts import get_object_or_404, redirect
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Url
from .serializers import UrlSerializer, UrlCreateSerializer


class UrlViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Url.objects.all()
    lookup_field = 'short_code'

    def get_serializer_class(self):
        if self.action == self.create.__name__:
            return UrlCreateSerializer

        return UrlSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        response_serializer = UrlSerializer(instance, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def expand(self, request, short_code=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

