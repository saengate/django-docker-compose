# from unittest.mock import MagicMock
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps_my_module.serializers import BlogSerializer
from apps_my_module.models import Blog


class TestBlogSerializer(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.data = {
            'name': 'pepito',
            'tagline': 'vaasdasdas dfdsfdsfdsf adsfadsf',
        }
        # instancia = Blog.objects.get(id=1)
        self.serializer = BlogSerializer(
            data=self.data,
        )

    def test_is_valid_when_ok_then_return_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_is_valid_when_error_then_return_data(self):
        del self.data['name']
        with self.assertRaises(ValidationError):
            self.assertFalse(self.serializer.is_valid(raise_exception=True))
        self.assertIn('name', self.serializer.errors)

    def test_save_when_ok_then_save_data(self):
        self.assertTrue(self.serializer.is_valid(raise_exception=True))
        instance = self.serializer.save()
        blog = Blog.objects.get(id=instance.id)
        self.assertIsInstance(blog, Blog)

    def test_update_when_ok_then_save_data(self):
        self.assertTrue(self.serializer.is_valid(raise_exception=True))
        instance = self.serializer.save()
        blog = Blog.objects.get(id=instance.id)
        self.assertIsInstance(blog, Blog)

        data = {
            'name': 'fulanito',
            'tagline': 'bbbbb bbb bb bb',
        }

        self.serializer = BlogSerializer(
            data=data,
            instance=instance,
        )
        self.assertTrue(self.serializer.is_valid(raise_exception=True))
        instance = self.serializer.save()
        blog = Blog.objects.get(id=instance.id)
        self.assertEqual(blog.name, data['name'])
        self.assertEqual(blog.tagline, data['tagline'])
