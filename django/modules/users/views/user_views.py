import logging

from django.conf import settings
from django.db import transaction
from django.http import HttpResponseRedirect
from rest_framework import permissions, status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import (
    RefreshJSONWebTokenView,
    ObtainJSONWebTokenView,
)

from modules.users.auth import UserLoginRateThrottle
from modules.users.models import User
from modules.users.serializers import (
    UserModelSerializer,
    UserSignUpSerializer,
)
from modules.users.serializers import CustomRefreshAuthTokenSerializer
from modules.users.utils.shortcuts import move_users_to_blacklist


logger = logging.getLogger(__name__)


class UserViewSet(generics.DestroyAPIView, viewsets.ViewSet):
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
        move_users_to_blacklist([self.request.user])
        self.request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomRefreshJSONWebTokenView(RefreshJSONWebTokenView):
    serializer_class = CustomRefreshAuthTokenSerializer


class CustomObtainJSONWebTokenView(ObtainJSONWebTokenView):
    throttle_classes = [UserLoginRateThrottle]
