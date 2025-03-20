from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Url
from .serializers import UrlSerializer, UrlCreateSerializer


class ShortenUrlView(APIView):
    """
    API view to shorten a URL
    """
    def post(self, request):
        serializer = UrlCreateSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.save()
            return Response(
                UrlSerializer(url, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpandUrlView(APIView):
    """
    API view to expand a shortened URL
    """
    def get(self, request, short_code):
        url = get_object_or_404(Url, short_code=short_code)
        serializer = UrlSerializer(url, context={'request': request})
        return Response(serializer.data)


def redirect_view(request, short_code):
    """
    View to redirect from short URL to original URL
    """
    url = get_object_or_404(Url, short_code=short_code)
    return redirect(url.original_url)
