import re

from django.contrib.auth import password_validation
from rest_framework.serializers import ValidationError


class PasswordValidator:

    MESSAGE = """
        La contraseña debe contener al menos una letra minúscula,
        una letra mayúscula, un número y un símbolo(-_.,@#$%).
    """

    def __call__(self, password):
        password_validation.validate_password(password)
        password_regex = re.compile(r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[-_.,@#$%])[\w\d@#$-_.,%]{8,64}$')  # NOQA
        if not password_regex.match(password):
            raise ValidationError(self.MESSAGE, code='invalid_password')
