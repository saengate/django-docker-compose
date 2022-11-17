import os

from datetime import (
    datetime,
    timedelta,
)
from config.core_settings import *  # NOQA

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Refer to secret from project Secrets usually PROJECTNAME_SECRET

SECRET_KEY = os.getenv('SECRET_KEY')

INSTALLED_APPS = INSTALLED_APPS + [  # NOQA
    'cforemoto',
    'fintoc_app',
]

AUTH_USER_MODEL = 'cforemoto.User'

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_payload',
    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_token',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'cforemoto.serializers.jwt_user_login_serializer',
    'JWT_EXPIRATION_DELTA': timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=1),
    'JWT_ALLOW_REFRESH': True,
    'JWT_DELETE_STALE_BLACKLISTED_TOKENS': True,
}

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
DOCS_NEAR_TO_EXPIRE_TEMPLATE = os.environ.get(
    'DOCS_NEAR_TO_EXPIRE_TEMPLATE', '--')
DOCS_EXPIRE_DOCUMENTS_TEMPLATE = os.environ.get(
    'DOCS_EXPIRE_DOCUMENTS_TEMPLATE', '--')
FORGOT_PASSWORD_TEMPLATE = os.environ.get('FORGOT_PASSWORD_TEMPLATE', '--')
USER_CONFIRMATION_TEMPLATE = os.environ.get('USER_CONFIRMATION_TEMPLATE', '--')
CEO_EMAIL_ADDRESS = os.environ.get('CEO_EMAIL_ADDRESS', '')
NO_REPLY_EMAIL_ADDRESS = (
    'no-reply@cforemoto.com',
    'CFOremoto',
)
SENDGRID_CATEGORIES = {
    'EXPIRED_DOCUMENTS': 'Expired Documents',
    'NEAR_TO_EXPIRE_DOCUMENTS': 'Near to expire documents',
    'PASSWORD_RECOVERY': 'Password Recovery',
    'USER_CONFIRMATION': 'User Confirmation',
}
SEGMENT_WRITE_KEY = os.environ.get('SEGMENT_WRITE_KEY')
CASH_FLOW_FORECAST_DAYS = 90

FINTOC_API_URL = 'https://api.fintoc.com/v1'
FINTOC_SECRET_KEY = os.environ.get('FINTOC_SECRET_KEY', '--')
FINTOC_PUBLIC_KEY = os.environ.get('FINTOC_PUBLIC_KEY', '--')
FINTOC_DEFAULT_SINCE_DATE = datetime(2020, 1, 1)

HEADER_WEBHOOK_N8N = os.environ.get('HEADER_WEBHOOK_N8N')
N8N_URL = os.environ.get('N8N_URL', 'http://cfo_n8n:5678/webhook-test')

CHITA_PROMOTIONAL_CODE = os.environ.get(
    'CHITA_PROMOTIONAL_CODE',
    'F8AS-ArS4-GRE8-As5G',
)
CHITA_URL = os.environ.get(
    'CHITA_URL',
    'http://0.0.0.0:7010/users/active_user/',
)
CHITA_HEADERS = os.environ.get('CHITA_HEADERS')

INVOICES_SII_CODES = [33, 34]
TICKETS_SII_CODES = [35, 38, 39, 41]
DEBITS_AND_CREDITS_NOTES_SII_CODES = [56, 61]
RELATED_SII_CODES = INVOICES_SII_CODES + TICKETS_SII_CODES + \
    DEBITS_AND_CREDITS_NOTES_SII_CODES

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Tiempo de espera antes de ejecutar las tareas programadas
# No hace falta esperar localmente, o ya se han descargado
# o es ambiente de pruebas
WAIT_FOR_FINTOC = {'seconds': 2}
DELAY_SECS_BETWEEN_TASK = 1
DEFAULT_FILE_STORAGE = 'utils.custom_storage.CustomStorage'

AUTHENTICATION_BACKENDS = [
    'apps_my_module.auth.AuthenticateBackend',
]

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
