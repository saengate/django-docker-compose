from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache


class GenericView(viewsets.ModelViewSet):
    queryset = None
    model = None
    serializer_class = None
    filter_fields = '__all__'
    ordering = 'id'
    cache_timeout = 10000

    def clean_cache(self, request):
        user_id = request.user.id
        list_cached = cache.keys(str(user_id) + '-*')
        for elem in list_cached:
            cache.delete(elem)

    def set_cache(self, request, *args, **kwargs):
        url_params = request.META['QUERY_STRING']
        user_id = request.user.id
        cache_key = str(user_id) + '-' + url_params
        if cache_key in cache:
            data = cache.get(cache_key)
        else:
            response = super().list(request, *args, **kwargs)
            data = response.data
            cache.set(cache_key, data, self.cache_timeout)
        return data

    def list(self, request, *args, **kwargs):
        data = self.set_cache(request, *args, **kwargs)
        return Response(data)

    def create(self, request, *args, **kwargs):
        self.clean_cache(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.clean_cache(request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.clean_cache(request)
        return super().destroy(request, *args, **kwargs)
