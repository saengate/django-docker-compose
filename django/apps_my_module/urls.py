from django.conf.urls import (
    url,
    include,
)
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    verify_jwt_token,
)
from rest_framework_jwt.blacklist.views import BlacklistView

from apps_my_module import views


# Routers provide a way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'custom', views.CustomViews, basename='custom_views')
router.register(r'blog', views.BlogViews, basename='blog_views')
router.register(r'author', views.AuthorViews, basename='author_views')
router.register(r'entry', views.EntryViews, basename='entry_views')

patterns = [
    url(r'^login/', obtain_jwt_token, name='login'),
    url(r'^logout/', BlacklistView.as_view({'post': 'create'})),
    url(r'^refresh_token/', views.CustomRefreshJSONWebTokenView.as_view()),
    url(r'^verify_token/', verify_jwt_token, name='verify_token'),
    url('users/password/', include(
        'django_rest_passwordreset.urls', namespace='password_reset')),
]


urlpatterns = [
    url('', include(patterns)),
    url('', include(router.urls)),
]

app_name = 'apps_my_module'
