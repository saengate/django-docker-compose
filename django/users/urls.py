from django.urls import (
    path,
    include,
)
from rest_framework import routers
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.blacklist.views import BlacklistView

from users import views


# Routers provide a way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet, basename='users')

patterns = [
    path('login/', views.CustomObtainJSONWebTokenView.as_view(), name='login'),
    path('logout/', BlacklistView.as_view({'post': 'create'})),
    path('refresh_token/', views.CustomRefreshJSONWebTokenView.as_view()),
    path('verify_token/', verify_jwt_token, name='verify_token'),
    path('users/password/', include(
        'django_rest_passwordreset.urls', namespace='password_reset')),
]


urlpatterns = [
    path('', include(patterns)),
    path('', include(router.urls)),
]

app_name = 'users'
