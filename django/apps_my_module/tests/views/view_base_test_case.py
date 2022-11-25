from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework_jwt.settings import api_settings

from apps_my_module.tests.factories import (
    UserFactory,
)


class ViewBaseTestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = UserFactory().create()
        self.client.force_login(self.user)

        self.jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self.jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = self.jwt_payload_handler(self.user)
        token = self.jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
