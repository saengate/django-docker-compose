import logging

from django.db.models import Q

from utils.date_utils import DateUtils
from apps_my_module.models import User


logger = logging.getLogger(__name__)


class UserInactive:

    def start(self, *args, **options):
        four_months_ago = DateUtils.rest_months_to_date(DateUtils.today(), 4)
        inactive_users = User.objects.filter(
            Q(
                last_login__isnull=True,
                date_joined__date__lte=four_months_ago,
            )
            | Q(last_login__date__lte=four_months_ago),
        ).delete()

        logger.info(f'inactive users {inactive_users}')
