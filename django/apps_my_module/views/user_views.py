import logging

from django.conf import settings
from django.db import transaction
from django.http import HttpResponseRedirect
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import RefreshJSONWebTokenView

from apps_my_module.models import User
from apps_my_module.serializers import (UserModelSerializer,
                                        UserSignUpSerializer)
# from apps_my_module.serializers import CustomRefreshAuthTokenSerializer
from apps_my_module.use_cases.shortcuts import move_users_to_blacklist
from utils.generic_views import GenericView

logger = logging.getLogger(__name__)


class UserViewSet(GenericView):

    serializer_class = UserModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_authenticators(self):
        if self.request.method == 'DELETE':
            self.authentication_classes = [JSONWebTokenAuthentication]
        return super().get_authenticators()

    @transaction.atomic
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        logger.info(f"Created new user {user}")  # NOQA
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def active_user(self, request):
        exists = User.objects.filter(
            email=request.data.get('email'),
            is_active=True,
        ).exists()
        return Response(exists, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def confirm(self, request):
        try:
            token = request.GET['verification_secret']
            user = User.objects.get(verification_secret=token)
        except (User.DoesNotExist, KeyError):
            logger.error("Token inválido")  # NOQA
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_confirmed = True
            user.save()
        redirect_url = settings.FRONTEND_URL
        return HttpResponseRedirect(redirect_to=redirect_url)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        self.request.user.delete()
        move_users_to_blacklist(self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomRefreshJSONWebTokenView(RefreshJSONWebTokenView):
    pass
    # serializer_class = CustomRefreshAuthTokenSerializer
