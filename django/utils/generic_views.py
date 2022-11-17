from rest_framework import (
    mixins,
    viewsets,
    generics,
    status,
)
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class GenericView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView,
        viewsets.ViewSet,
):
    queryset = None
    model = None
    serializer_class = None
    filter_fields = '__all__'
    ordering = 'id'
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return self.create(serializer, *args, **kwargs)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        id = request.data['id']
        if id:
            try:
                self.queryset = self.queryset.get(pk=id)
            except ObjectDoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                )
        if data.is_valid():
            return self.update(request, *args, **kwargs)
        else:
            return Response(
                data=data.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
