from django.urls import (
    path,
    include,
)
from rest_framework import routers

from apps_my_module import views


# Routers provide a way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'custom', views.CustomViews, basename='custom_views')
router.register(r'blog', views.BlogViews, basename='blog_views')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'apps_my_module'
