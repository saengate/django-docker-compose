from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username = f'{self.model.USERNAME_FIELD}__iexact'
        return self.get(**{case_insensitive_username: username})
