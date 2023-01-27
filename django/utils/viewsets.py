from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from django.core.cache import cache


def clean_cache(request):
    user_id = request.user.id
    list_cached = cache.keys(str(user_id) + '-*')
    for elem in list_cached:
        cache.delete(elem)


class CacheCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        clean_cache(request)
        return super().create(request, *args, **kwargs)


class CacheUpdateModelMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        clean_cache(request)
        return super().update(request, *args, **kwargs)


class CacheDestroyModelMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        clean_cache(request)
        return super().destroy(request, *args, **kwargs)


class CacheListModelMixin(mixins.ListModelMixin):
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


class GenericView(viewsets.GenericViewSet):
    queryset = None
    model = None
    serializer_class = None
    filter_fields = '__all__'
    ordering = 'id'
    cache_timeout = 10000
    throttle_scope = 'auth_views'
    throttle_classes = [ScopedRateThrottle]


class CivilModelViewSet(
    mixins.RetrieveModelMixin,
    CacheListModelMixin,
    GenericView,
):
    """ Read Only """
    pass


class HeroModelViewSet(
    CivilModelViewSet,
    CacheCreateModelMixin,
):
    """ Create and Read """
    pass


class DemiGodModelViewSet(
    HeroModelViewSet,
    CacheUpdateModelMixin,
):
    """ Create, Update and Read """
    pass


class GodModelViewSet(
    DemiGodModelViewSet,
    CacheDestroyModelMixin,
):
    """ All actions """
    pass
