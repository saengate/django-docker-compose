import jwt

from django.conf import settings
from rest_framework import serializers
from rest_framework_jwt.utils import (
    check_user,
    unix_epoch,
)
from rest_framework_jwt.compat import gettext_lazy as _
from rest_framework_jwt.serializers import RefreshAuthTokenSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


def check_payload(token):
    try:
        payload = JSONWebTokenAuthentication.jwt_decode_token(token)
    except jwt.ExpiredSignature:
        msg = _('Token has expired.')
        raise serializers.ValidationError(msg)
    except jwt.DecodeError:
        msg = _('Error decoding token.')
        raise serializers.ValidationError(msg)
    except jwt.InvalidTokenError:
        msg = _('Invalid token.')
        raise serializers.ValidationError(msg)

    return payload


class CustomRefreshAuthTokenSerializer(RefreshAuthTokenSerializer):

    def validate(self, data):
        token = data['token']

        payload = check_payload(token=token)
        user = check_user(payload=payload)

        # Get and check 'orig_iat'
        orig_iat = payload.get('orig_iat')

        if orig_iat is None:
            msg = _('orig_iat field not found in token.')
            raise serializers.ValidationError(msg)

        # Verify expiration
        refresh_limit = \
            settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA'].total_seconds()

        expiration_timestamp = orig_iat + refresh_limit
        now_timestamp = unix_epoch()

        if now_timestamp > expiration_timestamp:
            msg = _('Refresh has expired.')
            raise serializers.ValidationError(msg)

        new_payload = JSONWebTokenAuthentication.jwt_create_payload(user)
        new_payload['orig_iat'] = orig_iat

        return {
            'token':
                JSONWebTokenAuthentication.jwt_encode_payload(new_payload),
            'user':
                user,
            'issued_at':
                new_payload.get('iat', unix_epoch()),
        }
