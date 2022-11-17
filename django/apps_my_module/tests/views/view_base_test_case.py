import datetime

from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework_jwt.settings import api_settings

from apps_my_module.models import (
    User,
)
from apps_my_module.tests.base_test_case import BaseTestCase
from apps_my_module.tests.factories import (
    UserFactory,
)


class ViewBaseTestCase(APITestCase, BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin@admin.com',
            email='admin@admin.com',
            password='admin',
            is_confirmed=True,
        )
        self.client.force_login(self.user)

        self.jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self.jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = self.jwt_payload_handler(self.user)
        token = self.jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def do_get(self, url):
        return self.client.get(url)

    def do_post(self, url: str, body: dict = dict(), format='json'):
        return self.client.post(url, body, format=format)

    def do_patch(self, url: str, body: dict, format='json'):
        return self.client.patch(url, body, format=format)

    def do_put(self, url: str, body: dict, format='json'):
        return self.client.patch(url, body, format=format)

    def do_delete(self, url: str, body: dict = None):
        return self.client.delete(url, body, format='json')


class MockDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2010, 1, 1)

    @classmethod
    def timedelta(cls):
        pass
