from freezegun import freeze_time

from modules.apps_my_module.models import Entry
from modules.apps_my_module.tests.factories import AuthorFactory, BlogFactory
from modules.utils.date_utils import DateUtils


class EntryFactory:

    @freeze_time('2020-01-01')
    def __init__(
        self,
        **kwargs,
    ):
        self.blog_factory = BlogFactory()
        self.blog_instance = self.blog_factory.create()
        self.author_factory = AuthorFactory()
        self.author_instance = self.author_factory.create()
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
