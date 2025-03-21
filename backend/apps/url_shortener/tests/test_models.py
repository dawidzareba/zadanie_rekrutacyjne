from django.test import TestCase
from apps.url_shortener.models import Url
from constance.test import override_config


class UrlModelTest(TestCase):
    @override_config(SHORT_URL_LENGTH=3)
    def test_create_short_code(self):
        code1 = Url.create_short_code()
        code2 = Url.create_short_code()

        self.assertIsNotNone(code1)
        self.assertIsNotNone(code2)
        self.assertNotEqual(code1, code2)
        self.assertEqual(len(code1), 3)

    def test_create_short_code_with_custom_length(self):
        code = Url.create_short_code(length=8)
        self.assertEqual(len(code), 8)

    def test_string_representation(self):
        url = Url.objects.create(
            original_url="https://example.com", short_code="abc123"
        )
        self.assertEqual(str(url), "abc123 -> https://example.com")
