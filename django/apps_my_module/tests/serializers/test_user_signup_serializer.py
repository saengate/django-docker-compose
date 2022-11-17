from unittest.mock import MagicMock
from django.test import TestCase
from rest_framework.serializers import ValidationError as DRFValidationError

from utils.string_utils import (
    get_hash_md5_for_string,
    random_string,
)
from apps_my_module.serializers.exceptions import ServiceUnavailable
from apps_my_module.serializers import UserSignUpSerializer
from apps_my_module.use_cases.email_sender.exceptions import EmailSenderException


class TestUserSignupSerializer(TestCase):

    def setUp(self):
        self.data = {
            'email': 'A@a.cl',
            'password': '1234',
            'first_name': 'medusin',
            'last_name': 'teste',
            'username': 'A@a.com',
            'company_name': 'some company',
            'company_rut': '12312312-3',
        }
        self.invalid_password_code = {'code': 'invalid_password'}
        self.email_sender = MagicMock()
        self.serializer = UserSignUpSerializer(data=self.data)

    def test_validate_when_no_first_name_then_raise_exception(self):
        self.data['first_name'] = ''

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'blank'}, ct.exception.args[0]['first_name'][0].__dict__,
        )

        self.data.pop('first_name')
        self.serializer = UserSignUpSerializer(data=self.data)

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'required'},
            ct.exception.args[0]['first_name'][0].__dict__,
        )

    def test_validate_when_no_last_name_then_raise_exception(self):
        self.data['last_name'] = ''

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'blank'}, ct.exception.args[0]['last_name'][0].__dict__,
        )

        self.data.pop('last_name')
        self.serializer = UserSignUpSerializer(data=self.data)

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'required'},
            ct.exception.args[0]['last_name'][0].__dict__,
        )

    def test_validate_when_no_company_rut_then_raise_exception(self):
        self.data['company_rut'] = ''

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'blank'}, ct.exception.args[0]['company_rut'][0].__dict__,
        )

        self.data.pop('company_rut')
        self.serializer = UserSignUpSerializer(data=self.data)

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'required'},
            ct.exception.args[0]['company_rut'][0].__dict__,
        )

    def test_validate_when_no_username_then_raise_exception(self):
        self.data['username'] = ''

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'blank'}, ct.exception.args[0]['username'][0].__dict__,
        )

        self.data.pop('username')
        self.serializer = UserSignUpSerializer(data=self.data)

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'required'}, ct.exception.args[0]['username'][0].__dict__,
        )

    def test_validate_when_no_email_then_raise_exception(self):
        self.data['email'] = ''

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'blank'}, ct.exception.args[0]['email'][0].__dict__,
        )

        self.data.pop('email')
        self.serializer = UserSignUpSerializer(data=self.data)

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'required'}, ct.exception.args[0]['email'][0].__dict__,
        )

    def test_validate_when_no_password_then_raise_exception(self):
        self.data['password'] = ''

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'blank'}, ct.exception.args[0]['password'][0].__dict__,
        )

        self.data.pop('password')
        self.serializer = UserSignUpSerializer(data=self.data)

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'required'}, ct.exception.args[0]['password'][0].__dict__,
        )

    def test_validate_when_password_is_ok_then_return_input_data(self):
        result = self.serializer.is_valid(raise_exception=True)
        self.assertTrue(result)

    def test_validate_when_rut_is_invalid_then_raise_exception(self):
        self.data['company_rut'] = '33333333-2'

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'invalid_rut'},
            ct.exception.args[0]['company_rut']['rut'].__dict__,
        )
        self.data['company_rut'] = 'some fake rut'
        self.serializer = UserSignUpSerializer(data=self.data)

        with self.assertRaises(DRFValidationError) as ct:
            self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            {'code': 'invalid_rut'},
            ct.exception.args[0]['company_rut']['rut'].__dict__,
        )

    def test_create_when_email_error_then_return_ok_response(self):
        self.serializer = UserSignUpSerializer(
            data=self.data, email_sender=self.email_sender,
        )
        self.serializer.is_valid()
        response = self.serializer.save()
        self.email_sender.send.side_effect = EmailSenderException()

        self.serializer.is_valid(raise_exception=True)
        self.assertEqual(self.data['email'].lower(), response.email)
        self.assertEqual(
            get_hash_md5_for_string(self.data['email'].lower()),
            response.verification_secret,
        )

    def test_create_when_confirmation_is_ok_then_return_ok_response(self):
        self.serializer = UserSignUpSerializer(
            data=self.data, email_sender=self.email_sender,
        )
        self.serializer.is_valid()
        response = self.serializer.save()

        self.assertEqual(self.data['email'].lower(), response.email)
        self.assertEqual(
            get_hash_md5_for_string(self.data['email'].lower()),
            response.verification_secret,
        )
        self.email_sender.send.assert_called_once_with(response)

    def test_validate_when_password_is_lower_than_4_then_raise_exception(self):
        self.data['password'] = random_string(3)

        with self.assertRaises(DRFValidationError):
            self.serializer.is_valid(raise_exception=True)

        self.assertIn('password', self.serializer.errors)

    def test_validate_when_password_is_greater_than_64_then_raise_exception(
        self,
    ):
        self.data['password'] = random_string(65)

        with self.assertRaises(DRFValidationError):
            self.serializer.is_valid(raise_exception=True)

        self.assertIn('password', self.serializer.errors)
