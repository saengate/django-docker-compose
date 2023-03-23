from django.test import TestCase

from modules.apps_my_module.tests.factories import EntryFactory
from modules.apps_my_module.models import (
    Entry,
    Blog,
    Author,
    Comment,
)


class TestEntryModel(TestCase):
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
            ).filter(
                blog__name='bla_bla',
                blog__tagline='bla_bla',
                authors__email='bla@bla.cl',
            )
            for item in entries:
                item.authors.all()
                item.blog.name

    def setttings(create_entry=3):
        for _ in range(0, create_entry):
            EntryFactory().create()

    def test_querysets(self):
        EntryFactory().create()
        EntryFactory().create()
        EntryFactory().create()

        authors = Author.objects.prefetch_related(
            'entries',
            'entries__blog',
        ).all()
        with self.assertNumQueries(3):
            list(authors)
            for item in authors:
                entries = item.entries.all()
                list(entries)
                for entry in entries:
                    entry.blog.name

    def test_querysets_1(self):
        EntryFactory().create()
        EntryFactory().create()
        EntryFactory().create()

        blogs = Blog.objects.prefetch_related(
            'entries',
            'entries__authors',
        ).select_related(
            'comments',
        ).all()

        with self.assertNumQueries(3):
            list(blogs)
            for item in blogs:
                entries = item.entries.all()
                item.comments
                list(entries)
                for entry in entries:
                    entry.authors.name

    def test_querysets_2(self):
        EntryFactory().create()
        EntryFactory().create()
        EntryFactory().create()

        blogs = Blog.objects.select_related(
            'comments',
        ).all()

        with self.assertNumQueries(1):
            list(blogs)
            for item in blogs:
                item.comments

    def test_querysets_3(self):
        EntryFactory().create()
        EntryFactory().create()
        EntryFactory().create()

        authors = Author.objects.prefetch_related(
            'entries',
            'entries__blog__comments',
        ).all()

        with self.assertNumQueries(3):
            list(authors)
            for item in authors:
                entries = item.entries.all()
                list(entries)
                for entry in entries:
                    entry.blog.comments.comment

    def test_querysets_4(self):
        EntryFactory().create()
        EntryFactory().create()
        EntryFactory().create()

        entries = Entry.objects.select_related(
            'blog__comments',
        )

        with self.assertNumQueries(1):
            list(entries)
            for item in entries:
                item.blog.comments.comment
