import logging
# import django_heroku
# import sentry_sdk

from .base import *  # NOQA
from os import getenv
# from sentry_sdk.integrations.django import DjangoIntegration
# from sentry_sdk.integrations.logging import LoggingIntegration

from utils.color_logging import formatter


ENVIRONMENT = 'production'

# CONFIGS SENTRY PROD
""" SENTRY_DSN = getenv('SENTRY_DSN_BACKEND', '')

sentry_logging = LoggingIntegration(
    level=logging.ERROR,
    event_level=logging.ERROR,
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    environment=ENVIRONMENT,
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.2,
    send_default_pii=True,
) """

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = HOSTS = [
    '.execute-api.us-west-2.amazonaws.com',
    '.domain.com',
    '.cloudfront.net',
    '.herokuapp.com',
]

CORS_ALLOWED_ORIGIN_REGEXES = (
    r'^(.*)?\.domain\.com$',
)
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': getenv('DATABASE_HOST'),
        'PORT': getenv('DATABASE_PORT', '5432'),
        'NAME': getenv('DATABASE_NAME'),
        'USER': getenv('DATABASE_USER'),
        'PASSWORD': getenv('DATABASE_PASSWORD'),
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': formatter(),
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'class': 'utils.color_logging.NewLogger',
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

BACKEND_URL = 'https://backend.domain.com'
FRONTEND_URL = 'https://app.domain.com'

FEATURED_FLAGS_BASE_USERS = [
    'production@domain.com',
]

# django_heroku.settings(locals())
