from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.url_shortener.models import Url


class UrlViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = 'https://example.com'
        self.url_object = Url.objects.create(
            original_url=self.url,
            short_code='abc123'
        )
    
    def test_create_url(self):
        response = self.client.post(
            '/api/urls/',
            {'url': 'https://example.org'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_url', response.data)
        self.assertIn('short_code', response.data)
        self.assertEqual(response.data['original_url'], 'https://example.org')
        
        self.assertEqual(Url.objects.count(), 2)
        
    def test_retrieve_url(self):
        response = self.client.get(f'/api/urls/{self.url_object.short_code}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['original_url'], self.url)
        self.assertEqual(response.data['short_code'], self.url_object.short_code)
    
    def test_expand_url(self):
        response = self.client.get(f'/api/urls/{self.url_object.short_code}/expand/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['original_url'], self.url)


class GetOriginalUrlTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = 'https://example.com'
        self.url_object = Url.objects.create(
            original_url=self.url,
            short_code='abc123'
        )
    
    def test_get_original_url(self):
        response = self.client.get(f'/api/url/{self.url_object.short_code}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['original_url'], self.url)
    
    def test_get_original_url_not_found(self):
        response = self.client.get('/api/url/nonexistent')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
