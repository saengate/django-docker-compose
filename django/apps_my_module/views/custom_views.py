# from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class CustomViews(GenericViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def hello_world(self, request, format=None):
        return Response(
            {"message": "Hello, world!"},
            status=status.HTTP_200_OK,
        )
