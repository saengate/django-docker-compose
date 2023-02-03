from apps_my_module.models import Author


class AuthorFactory:

    def __init__(
        self,
        **kwargs,
    ):
        self.data = {
            'name': 'Author Test',
            'email': 'author@prueba.com',
        }
        self.data.update(**kwargs)

    def create(self) -> Author:
        return Author.objects.create(**self.data)
