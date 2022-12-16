# from unittest.mock import MagicMock
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from freezegun import freeze_time

from apps_my_module.serializers import (
    EntrySerializer,
    ReadEntrySerializer,
)
from apps_my_module.models import Entry
from apps_my_module.tests.factories import (
    BlogFactory,
    AuthorFactory,
)

from utils.date_utils import DateUtils


class TestEntrySerializer(TestCase):
    @freeze_time('2020-11-30')
    def setUp(self) -> None:
        super().setUp()
        self.blog_factory = BlogFactory()
        self.blog_instance = self.blog_factory.create()
        self.author_factory = AuthorFactory()
        self.author_instance = self.author_factory.create()
        self.data = {
            'blog': self.blog_instance.id,
            'headline': 'Blab bla',
            'body_text': 'Bla bla',
            'pub_date': DateUtils.today(),
            'mod_date': DateUtils.today(),
            'authors': [self.author_instance.id],
            'number_of_comments': 50,
            'number_of_pingbacks': 60,
            'rating': 20,
        }
        self.blog_serializer = EntrySerializer(
            data=self.data,
        )

    def test_is_valid_when_ok_then_return_data(self):
        self.assertTrue(self.blog_serializer.is_valid(raise_exception=True))

    def test_save_entry_when_ok_then_create_instance(self):
        self.assertTrue(self.blog_serializer.is_valid(raise_exception=True))
        self.blog_serializer.save()

    def test_read_entry_when_ok_then_get_instance(self):
        self.maxDiff = None
        self.blog_serializer.is_valid(raise_exception=True)
        instance_entry = self.blog_serializer.save()

        self.data['blog'] = self.blog_factory.data
        self.data['blog']['id'] = self.blog_instance.id
        self.data['authors'] = [self.author_factory.data]
        self.data['authors'][0]['id'] = self.blog_instance.id

        with self.assertNumQueries(1):
            serializer = ReadEntrySerializer(
                instance=instance_entry,
            )
            serializer.data['authors'][0]['name']
            serializer.data['blog']['name']
            """  self.assertDictContainsSubset(
                serializer.data,
                self.data,
            ) """

    """ def test_is_valid_when_error_then_return_data(self):
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
        self.assertEqual(blog.tagline, data['tagline']) """
