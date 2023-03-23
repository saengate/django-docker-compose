from modules.apps_my_module.models import Blog

from modules.apps_my_module.tests.factories.comment_factory import CommentFactory


class BlogFactory:

    def __init__(
        self,
        **kwargs,
    ):
        self.comment_factory = CommentFactory()
        self.comment_instance = self.comment_factory.create()

        self.data = {
            'name': 'Blog Test',
            'tagline': 'Bla Bla Bla',
            'comments': self.comment_instance,
        }
        self.data.update(**kwargs)

    def create(self) -> Blog:
        return Blog.objects.create(**self.data)
