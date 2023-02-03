import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.users'
    verbose_name = _('Users')

    def ready(self):
        logger.info('Users config app loaded')
        import modules.users.signals  # NOQA

        from modules.users.tasks.scheduler import add_scheduler_tasks
        add_scheduler_tasks()


logger = logging.getLogger(__name__)
