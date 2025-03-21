from django.test import TestCase
from apps.url_shortener.models import Url
from apps.url_shortener.serializers import UrlSerializer, UrlCreateSerializer
from rest_framework.test import APIRequestFactory


class UrlSerializerTest(TestCase):
    def setUp(self):
        self.url_object = Url.objects.create(
            original_url="https://example.com", short_code="abc123"
        )
        self.factory = APIRequestFactory()

    def test_url_serializer_contains_expected_fields(self):
        request = self.factory.get("/")
        serializer = UrlSerializer(
            instance=self.url_object, context={"request": request}
        )
        data = serializer.data

        self.assertIn("original_url", data)
        self.assertIn("short_code", data)
        self.assertIn("short_url", data)
        self.assertIn("created_at", data)

    def test_url_serializer_short_url_value(self):
        request = self.factory.get("/")
        serializer = UrlSerializer(
            instance=self.url_object, context={"request": request}
        )
        data = serializer.data

        expected_url = f"http://testserver/api/urls/url/{self.url_object.short_code}"
        self.assertEqual(data["short_url"], expected_url)


class UrlCreateSerializerTest(TestCase):
    def test_url_create_serializer_creates_url(self):
        data = {"url": "https://example.com"}
        serializer = UrlCreateSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        url_object = serializer.save()

        self.assertEqual(url_object.original_url, "https://example.com")
        self.assertIsNotNone(url_object.short_code)
        self.assertEqual(len(url_object.short_code), 6)
