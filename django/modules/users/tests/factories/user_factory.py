from modules.users.models import User


class UserFactory:

    def __init__(
        self,
        **kwargs,
    ):
        self.data = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'first_name': 'tester',
            'last_name': 'tester',
            'password': '@Somepass12',
        }
        self.data.update(**kwargs)

    def create(self) -> User:
        return User.objects.create_user(**self.data)
