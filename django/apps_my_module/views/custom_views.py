# from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps_my_module.serializers import CustomSerializer


class CustomViews(GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = CustomSerializer

    @action(detail=False, methods=['get', 'post'])
    def hello_world(self, request, format=None):
        data = {'message': 'Hello, world!'}

        if self.request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = {'message': serializer.data}
        return Response(
            data,
            status=status.HTTP_200_OK,
        )
