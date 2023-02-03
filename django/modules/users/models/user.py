from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from modules.users.models.managers import CustomUserManager
from modules.utils.date_utils import DateUtils


class User(AbstractUser):
    verification_secret = models.CharField(
        _('Verification secret'),
        max_length=256,
        blank=False,
        null=False,
    )
    is_confirmed = models.BooleanField(
        _('Confirmed'),
        default=False,
    )
    wrong_password_count = models.SmallIntegerField(
        _('Wrong password count'),
        default=0,
    )

    feature_flags = models.JSONField(
        _('Feature flags'),
        default=dict,
    )

    objects = CustomUserManager()

    def update_last_login(self, *args, **kwargs):
        self.last_login = DateUtils.now()
        self.wrong_password_count = 0
        self.save(update_fields=['last_login', 'wrong_password_count'])

    def __str__(self) -> str:
        return self.username


class UserToken(Token):
    key = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        if not self.key:
            payload = JSONWebTokenAuthentication.jwt_create_payload(
                self.user,
            )
            self.key = JSONWebTokenAuthentication.jwt_encode_payload(payload)
        return super().save(*args, **kwargs)
