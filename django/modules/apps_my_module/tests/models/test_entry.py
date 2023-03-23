from django.test import TestCase

from modules.apps_my_module.tests.factories import EntryFactory
from modules.apps_my_module.models import Entry


class EntryModel(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_add_entry_when_all_ok_then_return_instance(self):
        instance = EntryFactory().create()
        self.assertIsInstance(instance, Entry)

        with self.assertNumQueries(0):
            instance.authors.all()
            instance.blog.name

    def test_query_entry_when_filter_then_return_instance(self):
        EntryFactory().create()
        EntryFactory().create()
        EntryFactory().create()

        with self.assertNumQueries(4):
            entries = Entry.objects.all()
            for item in entries:
                item.authors.all()
                item.blog.name

    def test_select_releated_when_filter_then_return_instance(self):
        EntryFactory().create()
        EntryFactory().create()
        EntryFactory().create()

        with self.assertNumQueries(2):
            entries = Entry.objects.select_related(
                'blog',
            ).prefetch_related(
                'authors',
            ).all()
            for item in entries:
                item.authors.all()
                item.blog.name
