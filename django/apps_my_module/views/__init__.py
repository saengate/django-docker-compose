from apps_my_module.views.user_views import (CustomRefreshJSONWebTokenView,
                                             UserViewSet)
from apps_my_module.views.blog_views import BlogViews

__all__ = [
    'UserViewSet',
    'CustomRefreshJSONWebTokenView',
    'CustomViews',
    'BlogViews',
]
