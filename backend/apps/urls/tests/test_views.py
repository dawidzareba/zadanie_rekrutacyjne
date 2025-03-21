from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock
from django.core.cache import cache
from django.test.utils import override_settings

from apps.urls.models import ShortUrl


class UrlViewSetTest(APITestCase):
    def setUp(self):
        self.url = "https://example.com"
        self.url_object = ShortUrl.objects.create(
            original_url=self.url, short_code="abc123"
        )
        self.throttle_patcher = mock.patch(
            "rest_framework.throttling.ScopedRateThrottle.allow_request",
            return_value=True,
        )
        self.throttle_patcher.start()

    def tearDown(self):
        self.throttle_patcher.stop()

    def test_create_url(self):
        response = self.client.post(
            "/api/urls/", {"url": "https://example.org"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", response.data)
        self.assertIn("short_code", response.data)
        self.assertEqual(response.data["original_url"], "https://example.org")
        self.assertEqual(ShortUrl.objects.count(), 2)

    def test_retrieve_url(self):
        response = self.client.get(
            f"/api/urls/{self.url_object.short_code}", HTTP_ACCEPT="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["original_url"], self.url)
        self.assertEqual(response.data["short_code"], self.url_object.short_code)

    def test_retrieve_url_without_trailing_slash(self):
        response = self.client.get(f"/api/urls/{self.url_object.short_code}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["original_url"], self.url)
        self.assertEqual(response.data["short_code"], self.url_object.short_code)

    def test_retrieve_url_not_found(self):
        response = self.client.get("/api/urls/nonexistent")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ThrottlingTest(APITestCase):
    def setUp(self):
        self.url = "https://example.com"
        self.url_object = ShortUrl.objects.create(
            original_url=self.url, short_code="abc123"
        )

    def test_throttling_applied(self):
        from apps.urls.views import UrlViewSet
        from rest_framework.throttling import ScopedRateThrottle
        from django.conf import settings

        self.assertIn(ScopedRateThrottle, UrlViewSet.throttle_classes)
        self.assertIn("create", UrlViewSet.throttle_scope_map)
        self.assertIn("retrieve", UrlViewSet.throttle_scope_map)

        self.assertIn("url_create", settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"])
        self.assertIn("url_retrieve", settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"])


class CachingTest(APITestCase):
    def setUp(self):
        self.url = "https://example.com"
        self.url_object = ShortUrl.objects.create(
            original_url=self.url, short_code="abc123"
        )
        cache.clear()

        self.throttle_patcher = mock.patch(
            "rest_framework.throttling.ScopedRateThrottle.allow_request",
            return_value=True,
        )
        self.throttle_patcher.start()

    def tearDown(self):
        self.throttle_patcher.stop()
        cache.clear()

    def test_retrieve_caching(self):
        with self.assertNumQueries(1):
            response1 = self.client.get(f"/api/urls/{self.url_object.short_code}")
            self.assertEqual(response1.status_code, status.HTTP_200_OK)

        with self.assertNumQueries(0):
            response2 = self.client.get(f"/api/urls/{self.url_object.short_code}")
            self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertEqual(response1.data, response2.data)

    @override_settings(ROOT_URLCONF="config.urls")
    def test_cache_invalidation(self):
        response1 = self.client.get(f"/api/urls/{self.url_object.short_code}")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        new_url = "https://updated-example.com"
        self.url_object.original_url = new_url
        self.url_object.save()

        with self.assertNumQueries(0):
            response2 = self.client.get(f"/api/urls/{self.url_object.short_code}")
            self.assertEqual(response2.data["original_url"], self.url)

        cache.clear()
        with self.assertNumQueries(1):
            response3 = self.client.get(f"/api/urls/{self.url_object.short_code}")
            self.assertEqual(response3.data["original_url"], new_url)  # New URL
