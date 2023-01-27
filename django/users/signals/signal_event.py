from django.dispatch import receiver
from django.contrib.auth.signals import user_login_failed

from users.models import User


@receiver(user_login_failed)
def failed_user_login(**kwargs):
    username = kwargs.get('credentials').get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        pass
    else:
        user.wrong_password_count += 1
        if user.wrong_password_count >= 3:
            user.is_active = False
        user.save(update_fields=['is_active', 'wrong_password_count'])
