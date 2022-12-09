from apps_my_module.views.blog_views import BlogViews
from apps_my_module.views.custom_views import CustomViews
from apps_my_module.views.user_views import (CustomRefreshJSONWebTokenView,
                                             UserViewSet)

__all__ = [
    'UserViewSet',
    'CustomRefreshJSONWebTokenView',
    'CustomViews',
    'BlogViews',
]
