# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps_my_module.serializers import AuthorSerializer
from apps_my_module.models import Author
from utils.viewsets import GodModelViewSet


class AuthorViews(GodModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AuthorSerializer
    model = Author
    queryset = Author.objects.all()
