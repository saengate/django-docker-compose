from apps_my_module.models import Blog


class BlogFactory:

    def __init__(
        self,
        **kwargs,
    ):
        self.data = {
            'name': 'Blog Test',
            'tagline': 'Bla Bla Bla',
        }
        self.data.update(**kwargs)

    def create(self) -> Blog:
        return Blog.objects.create(**self.data)
