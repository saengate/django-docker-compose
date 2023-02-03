from unittest import TestCase
from rest_framework.serializers import ValidationError

from modules.apps_my_module.serializers.validators import RutValidator


class TestRutValidator(TestCase):
    def setUp(self) -> None:
        self.validate = RutValidator()

    def test_validate_when_no_rut_then_raise_exception(self):
        rut = ''
        self.assertRaises(ValidationError, lambda: self.validate(rut))

    def test_validate_when_rut_is_none_then_raise_exception(self):
        rut = None
        self.assertRaises(ValidationError, lambda: self.validate(rut))

    def test_validate_when_rut_is_not_str_then_raise_exception(self):
        rut = 9
        self.assertRaises(ValidationError, lambda: self.validate(rut))

    def test_validate_when_rut_has_not_rut_format_then_raise_exception(self):
        rut = '12/7'
        self.assertRaises(ValidationError, lambda: self.validate(rut))

    def test_validate_when_rut_identifier_is_not_int_then_raise_exception(self):
        rut = 'some_stuff-9'
        self.assertRaises(ValidationError, lambda: self.validate(rut))

    def test_validate_when_identifier_is_lower_than_1MM_then_raise_error(self):
        rut = '1-1'
        self.assertRaises(ValidationError, lambda: self.validate(rut))

    def test_validate_when_verifier_len_greater_than_1_then_raise_error(self):
        rut = '12312312-33'
        self.assertRaises(ValidationError, lambda: self.validate(rut))

    def test_validate_when_rut_has_invalid_verifier_then_raise_exception(self):
        rut = '12312312-5'
        self.assertRaises(ValidationError, lambda: self.validate(rut))

    def test_validate_when_rut_has_valid_with_7_digits_then_ok(self):
        rut = '6846931-7'
        self.assertTrue(self.validate(rut))

    def test_validate_when_rut_has_valid_with_8_digits_then_ok(self):
        rut = '12708498-k'
        self.assertTrue(self.validate(rut))
        rut = '12708498-K'
        self.assertTrue(self.validate(rut))
