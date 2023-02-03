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

from django.urls import (
    path,
    re_path,
    include,
)
from django.conf import settings


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('modules.users.urls', namespace='users')),
    path('api/v1/', include(
        'modules.apps_my_module.urls',
        namespace='apps_my_module',
    )),
    path('django-rq/', include('django_rq.urls')),
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
        path(
            'favicon.ico',
            RedirectView.as_view(
                url=settings.STATIC_URL + 'apps_my_module/images/favicon.ico',
            ),
        ),
        re_path(r'^swagger(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0),
                name='schema-json'),
        re_path(r'^swagger/$',
                schema_view.with_ui('swagger', cache_timeout=0),
                name='schema-swagger-ui'),
        re_path(r'^redoc/$',
                schema_view.with_ui('redoc', cache_timeout=0),
                name='schema-redoc'),
    ]
