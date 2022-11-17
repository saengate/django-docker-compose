from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Servicio temporalmente no disponible. Por favor, intente más tarde.'
    default_code = 'service_unavailable'
