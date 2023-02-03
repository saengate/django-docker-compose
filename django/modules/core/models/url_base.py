import requests
from urllib.parse import urlparse, urlunparse

from django.db import models
from django.conf import settings


class UrlBase(models.Model):
    class Meta:
        abstract = True

    def get_url(self):
        if hasattr(self.get_url_path, 'dont_recurse'):
            raise NotImplementedError
        try:
            path = self.get_url_path()
        except NotImplementedError:
            raise
        return settings.BACKEND_URL + path
    get_url.dont_recurse = True

    def get_url_path(self):
        if hasattr(self.get_url, 'dont_recurse'):
            raise NotImplementedError
        try:
            url = self.get_url()
        except NotImplementedError:
            raise
        bits = urlparse(url)
        return urlunparse(('', '') + bits[2:])
    get_url_path.dont_recurse = True

    def get_absolute_url(self):
        return self.get_url()
