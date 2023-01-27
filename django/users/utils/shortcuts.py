from django.http import Http404

from rest_framework_jwt.blacklist.models import BlacklistedToken
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from jwt.exceptions import ExpiredSignatureError

from utils.date_utils import DateUtils
from users.models import UserToken


def move_users_to_blacklist(users):
    BlacklistedToken.objects.delete_stale_tokens()
    blacklist_tokens_list = []

    for user in users:
        try:
            token = user.auth_token.key
            token_decode = JSONWebTokenAuthentication.jwt_decode_token(token)
        except (UserToken.DoesNotExist, ExpiredSignatureError):
            continue

        expires_at = DateUtils().utcfromtimestamp(token_decode['exp'])
        expires_at = DateUtils().make_aware(expires_at)

        blacklist_token = {
            'token': token,
            'user': user,
            'expires_at': expires_at,
        }

        blacklist_tokens_list.append(BlacklistedToken(**blacklist_token))

    if blacklist_tokens_list:
        BlacklistedToken.objects.bulk_create(blacklist_tokens_list)
