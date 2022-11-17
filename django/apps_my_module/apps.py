import logging

from django.apps import AppConfig


logger = logging.getLogger(__name__)


class AppsMyModuleConfig(AppConfig):
    name = 'apps_my_module'
    verbose_name = 'AppsMyModule App'

    def ready(self):
        logger.info('AppsMyModule config app loaded')
        import apps_my_module.signals  # NOQA

        from apps_my_module.tasks.scheduler import add_scheduler_tasks
        add_scheduler_tasks()
