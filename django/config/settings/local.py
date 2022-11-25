import pygments
import os

from .base import *  # NOQA
from utils.color_logging import formatter

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENVIRONMENT = 'develop'

INSTALLED_APPS = INSTALLED_APPS + [  # NOQA
    'drf_yasg',
]

HOSTS = ['127.0.0.1', '0.0.0.0', 'localhost', 'backend']

ALLOWED_HOSTS = ['*']

# CORS config https://pypi.org/project/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True

# To allow default credentials
CORS_ALLOW_CREDENTIALS = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.getenv('DATABASE_HOST', 'db'),
        'PORT': '5432',
        'NAME': 'play_django',
        'USER': 'userdb',
        'PASSWORD': 'password',
    },
}

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'staticfiles'),  # NOQA
]

# https://django-extensions.readthedocs.io/en/latest/shell_plus.html
# ./manage.py shell_plus --notebook
# Always use IPython for shell_plus
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True
# Truncate sql queries to this number of characters (this is the default)
SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000
# To disable truncation of sql queries use
SHELL_PLUS_PRINT_SQL_TRUNCATE = None
# Specify sqlparse configuration options when printing sql queries to the console
SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = dict(
    reindent_aligned=True,
    truncate_strings=500,
)

# Specify Pygments formatter and configuration options when printing sql queries to the console
SHELL_PLUS_PYGMENTS_FORMATTER = pygments.formatters.TerminalFormatter
SHELL_PLUS_PYGMENTS_FORMATTER_KWARGS = {}

# Additional IPython arguments to use
IPYTHON_ARGUMENTS = [
    '--ext', 'django_extensions.management.notebook_extension',
    '--debug',
]

IPYTHON_KERNEL_DISPLAY_NAME = "Django Shell-Plus"
# Additional Notebook arguments to use
NOTEBOOK_ARGUMENTS = []
NOTEBOOK_KERNEL_SPEC_NAMES = ["python3", "python"]

NOTEBOOK_ARGUMENTS = [
    '--allow-root',
    '--ip', '0.0.0.0',
    '--port', '7001',
]

# LOGS
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

""" 'handlers': {
    'file': {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': '/var/log/apps_my_module/apps_my_module.log',
        'maxBytes': 1024 * 1024 * 10,  # 10MB
        'backupCount': 5,
        'formatter': 'standard',
    },
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'standard',
    },
}, """
BACKEND_URL = 'http://0.0.0.0:7010'
FRONTEND_URL = 'http://0.0.0.0'

FEATURED_FLAGS_BASE_USERS = [
    'localuser@localhost.com',
]
