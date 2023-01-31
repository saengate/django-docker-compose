from django.db import models
from django.contrib.auth.models import AbstractUser
from modules.users.models.managers import CustomUserManager
from rest_framework.authtoken.models import Token
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from modules.utils.date_utils import DateUtils


class User(AbstractUser):
    verification_secret = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )
    is_confirmed = models.BooleanField(
        default=False,
    )
    wrong_password_count = models.SmallIntegerField(
        default=0,
    )

    feature_flags = models.JSONField(default=dict)

    objects = CustomUserManager()

    def update_last_login(self, *args, **kwargs):
        self.last_login = DateUtils.now()
        self.wrong_password_count = 0
        self.save(update_fields=['last_login', 'wrong_password_count'])


class UserToken(Token):
    key = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        if not self.key:
            payload = JSONWebTokenAuthentication.jwt_create_payload(
                self.user,
            )
            self.key = JSONWebTokenAuthentication.jwt_encode_payload(payload)
        return super().save(*args, **kwargs)
