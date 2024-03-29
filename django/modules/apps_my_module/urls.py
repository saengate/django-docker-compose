from django.urls import (
    path,
    include,
)
from rest_framework import routers

from modules.apps_my_module import views


# Routers provide a way of automatically determining the URL conf.
router = routers.SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'apps_my_module'
