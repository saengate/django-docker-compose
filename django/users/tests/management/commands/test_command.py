import sys
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from users.models import (
    User,
    UserToken,
)


class CommandTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        suppress_text = StringIO()
        sys.stdout = suppress_text

    def tearDown(self) -> None:
        super().tearDown()
        sys.stdout = sys.__stdout__

    def test_call_when_not_user_then_return_string_no_users(self):
        out = StringIO()
        call_command('all_user_tokens_expire', stdout=out)
        self.assertIn('No hay usuarios activos', out.getvalue())

    def test_call_when_one_user_then_return_string_kill_tokens(self):
        user = User.objects.create_user(
            username='admin',
            email='admin@admin.com',
            password='admin',
        )
        UserToken.objects.create(user=user)
        out = StringIO()
        call_command('all_user_tokens_expire', stdout=out)
        self.assertIn(
            '¡Todos los token han sido agregados a la lista negra!',
            out.getvalue(),
        )

    def test_call_when_users_then_return_string_kill_tokens(self):
        users_list = [
            User(**{
                'username': 'admin',
                'email': 'admin@admin.com',
                'password': 'admin',
            }),
            User(**{
                'username': 'admin1',
                'email': 'admin1@admin.com',
                'password': 'admin',
            }),
        ]

        users = User.objects.bulk_create(users_list)
        [UserToken.objects.create(user=user) for user in users]

        out = StringIO()
        call_command('all_user_tokens_expire', stdout=out)
        self.assertIn(
            '¡Todos los token han sido agregados a la lista negra!',
            out.getvalue(),
        )
