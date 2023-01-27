# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from apps_my_module.serializers import (
    EntrySerializer,
    ReadEntrySerializer,
)
from apps_my_module.models import Entry
from utils.viewsets import GodModelViewSet


class EntryViews(GodModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = EntrySerializer
    model = Entry
    queryset = Entry.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadEntrySerializer
        return super().get_serializer_class()
