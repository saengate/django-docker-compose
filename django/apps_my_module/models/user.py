from django.db import models
from django.contrib.auth.models import AbstractUser
from apps_my_module.models.managers import CustomUserManager
from rest_framework.authtoken.models import Token
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class User(AbstractUser):
    verification_secret = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )

    feature_flags = models.JSONField(default=dict)

    objects = CustomUserManager()


class UserToken(Token):
    key = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        if not self.key:
            payload = JSONWebTokenAuthentication.jwt_create_payload(
                self.user,
            )
            self.key = JSONWebTokenAuthentication.jwt_encode_payload(payload)
        return super().save(*args, **kwargs)
