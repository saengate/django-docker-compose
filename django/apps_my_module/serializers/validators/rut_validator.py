import re

from rest_framework.serializers import ValidationError


class RutValidator:
    MESSAGE = {'rut': 'El rut ingresado es inválido.'}
    CODE = 'invalid_rut'
    INVALID_RUT_EXC = ValidationError(MESSAGE, code=CODE)

    def _get_verifier(self, rut: int):
        value = 11 - sum([
            int(a) * int(b) for a, b in zip(str(rut).zfill(8), '32765432')
        ]) % 11
        return {10: 'K', 11: '0'}.get(value, str(value))

    def format(self, rut: int):
        return '{0}-{1}'.format(rut, self._get_verifier(rut))

    def _is_formatted_rut(self, formatted_rut):
        return re.match(r'^\d+\.\d+\.\d+-\w$', formatted_rut)

    def __call__(self, rut_str):
        if not rut_str or not isinstance(rut_str, str):
            raise self.INVALID_RUT_EXC

        if self._is_formatted_rut(rut_str):
            rut_str = rut_str.replace('.', '')

        parts = rut_str.split('-')

        if not len(parts) == 2:
            raise self.INVALID_RUT_EXC

        try:
            rut = int(parts[0])
        except ValueError:
            raise self.INVALID_RUT_EXC

        if rut < 1000000:
            raise self.INVALID_RUT_EXC

        if not len(parts[1]) == 1:
            raise self.INVALID_RUT_EXC

        digit = parts[1].upper()

        is_valid = digit == self._get_verifier(rut)
        if not is_valid:
            raise self.INVALID_RUT_EXC
        return is_valid
