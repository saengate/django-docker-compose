# from unittest.mock import MagicMock
from django.test import TestCase
from freezegun import freeze_time

from apps_my_module.serializers import (
    EntrySerializer,
    ReadEntrySerializer,
)
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
            'pub_date': DateUtils.get_today_as_str(),
            'mod_date': DateUtils.get_today_as_str(),
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

        expected = self.data

        expected['blog'] = self.blog_factory.data
        expected['blog']['id'] = self.blog_instance.id
        expected['authors'] = [self.author_factory.data]
        expected['authors'][0]['id'] = self.blog_instance.id

        with self.assertNumQueries(1):
            serializer = ReadEntrySerializer(
                instance=instance_entry,
            )
            output = serializer.data
            del output['id']
            output['blog'] = dict(output['blog'])
            output['authors'][0] = dict(output['authors'][0])
            self.assertDictEqual(
                output,
                expected,
            )
