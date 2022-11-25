from apps_my_module.models import User


class UserFactory:

    def __init__(
        self,
        **kwargs,
    ):
        self.data = {
            'username': 'admin@admin.com',
            'first_name': 'tester',
            'last_name': 'tester',
            'password': '@Somepass12',
            'verification_secret': '124Token',
            'is_confirmed': True,
        }
        self.data.update(**kwargs)

    def create(self) -> User:
        return User.objects.create_user(**self.get_dict())
