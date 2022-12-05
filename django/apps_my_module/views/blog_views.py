# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps_my_module.serializers import BlogSerializer
from apps_my_module.models import Blog
from utils.generic_views import GenericView


class BlogViews(GenericView):
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer
    model = Blog
    queryset = Blog.objects.all()