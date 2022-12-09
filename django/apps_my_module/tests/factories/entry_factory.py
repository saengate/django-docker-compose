from freezegun import freeze_time

from apps_my_module.models import Entry
from apps_my_module.tests.factories import AuthorFactory, BlogFactory
from utils.date_utils import DateUtils


class EntryFactory:

    @freeze_time('2020-01-01')
    def __init__(
        self,
        **kwargs,
    ):
        self.blog_instance = BlogFactory().create()
        self.author_instance = AuthorFactory().create()
        self.data = {
            'blog': self.blog_instance,
            'headline': 'Bla Bla',
            'body_text': 'Bla Bla',
            'pub_date': DateUtils.today(),
            'mod_date': DateUtils.today(),
            'number_of_comments': 99,
            'number_of_pingbacks': 99,
            'rating': 10,
        }
        self.data.update(**kwargs)

    def create(self) -> Entry:
        entry = Entry.objects.create(**self.data)
        entry.authors.add(self.author_instance)
        return entry
