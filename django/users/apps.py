import logging
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Users App'

    def ready(self):
        logger.info('Users config app loaded')
        import users.signals  # NOQA

        from users.tasks.scheduler import add_scheduler_tasks
        add_scheduler_tasks()


logger = logging.getLogger(__name__)
