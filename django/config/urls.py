"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls import (
    url,
    include,
)
from django.conf import settings


urlpatterns = [
    url('i18n/', include('django.conf.urls.i18n')),
    url('', include('apps_my_module.urls', namespace='apps_my_module')),
    url('django-rq/', include('django_rq.urls')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static
    from django.views.generic.base import RedirectView
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title='Snippets API',
            default_version='v1',
            description='Test description',
            terms_of_service='https://www.google.com/policies/terms/',
            contact=openapi.Contact(email='contact@snippets.local'),
            license=openapi.License(name='BSD License'),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    # tell gunicorn where static files are in dev mode
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + 'images/',
        document_root=os.path.join(settings.MEDIA_ROOT, 'images'),
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=os.path.join(settings.STATIC_ROOT),
    )
    urlpatterns += [
        url(
            'favicon.ico$',
            RedirectView.as_view(
                url=settings.STATIC_URL + 'cforemoto/images/favicon.ico',
            ),
        ),
        url(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
        url(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
        url(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    ]
