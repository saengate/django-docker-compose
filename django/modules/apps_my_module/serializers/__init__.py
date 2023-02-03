from modules.apps_my_module.serializers.custom_serializer import (
    CustomSerializer,
)
from modules.apps_my_module.serializers.blog_serializer import BlogSerializer
from modules.apps_my_module.serializers.author_serializer import (
    AuthorSerializer,
)

__all__ = [
    'AuthorSerializer',
    'BlogSerializer',
    'CustomSerializer',
]
