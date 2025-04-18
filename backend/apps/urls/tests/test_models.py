from django.test import TestCase
from unittest.mock import patch
from apps.urls.models import ShortUrl
from constance.test import override_config


class UrlModelTest(TestCase):
    @override_config(SHORT_URL_LENGTH=3)
    def test_create_short_code(self):
        code1 = ShortUrl.create_short_code()
        code2 = ShortUrl.create_short_code()

        self.assertIsNotNone(code1)
        self.assertIsNotNone(code2)
        self.assertNotEqual(code1, code2)
        self.assertEqual(len(code1), 3)

    def test_create_short_code_with_custom_length(self):
        code = ShortUrl.create_short_code(length=8)
        self.assertEqual(len(code), 8)

    @override_config(SHORT_URL_LENGTH=3)
    def test_process_short_code_collision(self):
        known_code = "aaa"
        ShortUrl.objects.create(
            original_url="https://example.com", short_code=known_code
        )

        with patch("random.choice", return_value="a"):
            code = ShortUrl._process_short_code(length=3)
            self.assertIsNone(code)

    def test_process_short_code_success(self):
        with patch("random.choice", return_value="x"):
            code = ShortUrl._process_short_code(length=5)
            self.assertEqual(code, "xxxxx")

    def test_string_representation(self):
        url = ShortUrl.objects.create(
            original_url="https://example.com", short_code="abc123"
        )
        self.assertEqual(str(url), "abc123 -> https://example.com")
