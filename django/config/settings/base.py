import os
from datetime import timedelta

from config.core_settings import *  # NOQA

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Refer to secret from project Secrets usually PROJECTNAME_SECRET

SECRET_KEY = get_secret('SECRET_KEY')

INSTALLED_APPS = INSTALLED_APPS + [  # NOQA
    'modules.users',
    'modules.apps_my_module',
]

AUTH_USER_MODEL = 'users.User'

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_payload',
    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_token',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'users.serializers.jwt_user_login_serializer',
    'JWT_EXPIRATION_DELTA': timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=1),
    'JWT_ALLOW_REFRESH': True,
    'JWT_DELETE_STALE_BLACKLISTED_TOKENS': True,
}

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
FORGOT_PASSWORD_TEMPLATE = os.environ.get('FORGOT_PASSWORD_TEMPLATE', '--')
USER_CONFIRMATION_TEMPLATE = os.environ.get('USER_CONFIRMATION_TEMPLATE', '--')

SENDGRID_CATEGORIES = {
    'PASSWORD_RECOVERY': 'Password Recovery',
    'USER_CONFIRMATION': 'User Confirmation',
}
SEGMENT_WRITE_KEY = os.environ.get('SEGMENT_WRITE_KEY')

DELAY_SECS_BETWEEN_TASK = 1
DEFAULT_FILE_STORAGE = 'utils.custom_storage.CustomStorage'

AUTHENTICATION_BACKENDS = [
    'users.auth.AuthenticateBackend',
]

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
