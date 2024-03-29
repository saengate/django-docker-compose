"""
WSGI config for mysite django.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


environment = os.getenv('ENV', 'local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings.' + environment)
application = get_wsgi_application()
