from apps_my_module.views.blog_views import BlogViews
from apps_my_module.views.entry_views import EntryViews
from apps_my_module.views.author_views import AuthorViews
from apps_my_module.views.custom_views import CustomViews
from apps_my_module.views.user_views import (CustomRefreshJSONWebTokenView,
                                             UserViewSet)

__all__ = [
    'UserViewSet',
    'EntryViews',
    'CustomRefreshJSONWebTokenView',
    'CustomViews',
    'BlogViews',
    'AuthorViews',
]
