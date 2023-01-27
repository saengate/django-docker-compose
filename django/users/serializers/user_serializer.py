import logging

from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from asgiref.sync import sync_to_async

from utils.string_utils import get_hash_md5_for_string
from utils.date_utils import DateUtils
# from users.utils.email_sender import UserConfirmationEmail
# from users.serializers.validators import RutValidator
from users.models import (
    User,
    UserToken,
)


logger = logging.getLogger(__name__)


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'feature_flags',
        )


class UserSignUpSerializer(serializers.Serializer):

    email = serializers.EmailField(
        max_length=250,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="El correo ingresado ya se encuentra registrado",  # NOQA
            lookup='iexact',
        )],
    )
    username = serializers.CharField(
        max_length=250,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="El usuario ya se encuentra registrado",  # NOQA
            lookup='iexact',
        )],
    )

    password = serializers.CharField(min_length=4, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=100)

    # rut = serializers.CharField(validators=[RutValidator()])
    token = serializers.CharField(
        max_length=100,
        required=False,
    )

    class Meta:
        validators = []

    def __init__(self, *args, **kwargs):
        """ self.mailer = kwargs.pop(
            'email_sender', None) or UserConfirmationEmail() """
        super().__init__(*args, **kwargs)

    def create(self, data):
        data['email'] = data['email'].lower()
        data['username'] = data['username'].lower()
        data['verification_secret'] = get_hash_md5_for_string(data['email'])

        user = User.objects.create_user(**data)

        if not user.is_confirmed:
            # sync_to_async(self.__send_confirmation_email(user))
            pass

        return user

    def __send_confirmation_email(self, user):
        try:
            self.mailer.send(user)
        except Exception as e:
            logger.error(f'send confirmation mail error: {e}')


def jwt_user_login_serializer(token, user=None, request=None, issued_at=None):
    """
    Return data ready to be passed to serializer.

    Override this function if you need to include any additional data for
    serializer.

    Note that we are using `pk` field here - this is for forward compatibility
    with drf add-ons that might require `pk` field in order (eg. jsonapi).
    """

    user.update_last_login()
    UserToken.objects.update_or_create(
        user=user,
        defaults={'key': token},
    )

    return {
        'token': token,
        'user': UserModelSerializer(user, context={'request': request}).data,
        'exp': DateUtils.now() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA'],
        'orig_iat': issued_at,
    }
