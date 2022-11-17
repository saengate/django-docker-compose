import json
import sys
from io import StringIO

from django.urls import reverse
from django.conf import settings
from django.core.management import call_command
from unittest.mock import patch

from apps_my_module.tests.views.view_base_test_case import ViewBaseTestCase
from apps_my_module.use_cases.email_sender.exceptions import EmailSenderException
from apps_my_module.models import (
    User,
)
from utils.string_utils import random_string


class TestUserView(ViewBaseTestCase):

    def setUp(self):
        super().setUp()
        self.signup_url = '/users/signup/'
        self.login_url = '/login/'
        self.confirm_url = '/users/confirm/'
        self.recovery_url = '/users/password_recovery/'
        self.forgot_password_url = '/users/forgot_password/'
        self.delete_url = '/users/'
        self.username = 'a@a.com'
        self.login_data = {
            'username': 'A@a.com',
            'password': '1234',
        }
        self.registration = {
            'first_name': 'medusin',
            'last_name': 'cfo',
            'company_name': 'some company',
            'company_rut': '12312312-3',
            'email': 'A@a.com',
        }
        suppress_text = StringIO()
        sys.stdout = suppress_text

    def tearDown(self) -> None:
        super().tearDown()
        sys.stdout = sys.__stdout__
