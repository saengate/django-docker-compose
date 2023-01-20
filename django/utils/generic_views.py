from rest_framework import (
    viewsets,
    generics,
    status,
    mixins,
)
from rest_framework.response import Response
from django.core.cache import cache


class GenericView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView,
    viewsets.ViewSet,
):
    queryset = None
    model = None
    serializer_class = None
    filter_fields = '__all__'
    ordering = 'id'

    def clean_cache(self, request):
        user_id = request.user.id
        list_cached = cache.keys(str(user_id) + '-*')
        for elem in list_cached:
            cache.delete(elem)

    def list_cache(self, request, timeout, *args, **kwargs):
        url_params = request.META['QUERY_STRING']
        user_id = request.user.id
        cache_key = str(user_id) + '-' + url_params
        if cache_key in cache:
            intermediate_data = cache.get(cache_key)
            data = intermediate_data
        else:
            intermediate_data = self.list(request, *args, **kwargs)
            data = intermediate_data.data
            cache.set(cache_key, data, timeout)
        return data

    def list_response_cache(
        self,
        request,
        timeout=20000,
        status=status.HTTP_200_OK,
        *args,
        **kwargs,
    ):
        data = self.list_cache(request, timeout, *args, **kwargs)
        headers = self.get_success_headers(data)
        return Response(
            data,
            status=status,
            headers=headers,
        )

    def get(self, request, *args, **kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list_cache(request, 10000, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.clean_cache(request)
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.clean_cache(request)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.clean_cache(request)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.clean_cache(request)
        return self.destroy(request, *args, **kwargs)
