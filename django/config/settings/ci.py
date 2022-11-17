from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ENVIRONMENT = 'ci'

HOSTS = ['127.0.0.1']

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres_buildpack_db',
    },
}

BACKEND_URL = 'http://0.0.0.0:7010'
FRONTEND_URL = 'http://127.0.0.1'

FEATURED_FLAGS_BASE_USERS = []
