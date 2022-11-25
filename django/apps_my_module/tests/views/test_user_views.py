import sys
from io import StringIO

from apps_my_module.tests.views.view_base_test_case import ViewBaseTestCase


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
