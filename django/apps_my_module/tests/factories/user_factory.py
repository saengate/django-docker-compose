from apps_my_module.models import User


class UserFactory:

    def __init__(self, username='a@a.com'):
        self.first_name = 'medusin'
        self.last_name = 'teste'
        self.username = username
        self.password = '@Somepass12'
        self.verification_secret = '124'
        self.is_confirmed = True

    def get_dict(self) -> dict:
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password': self.password,
            'verification_secret': self.verification_secret,
            'is_confirmed': True,
        }

    def create(self) -> User:
        return User.objects.create(**self.get_dict())
