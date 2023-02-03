import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class AppsMyModuleConfig(AppConfig):
    name = 'modules.apps_my_module'
    verbose_name = _('AppsMyModule')

    def ready(self):
        logger.info('AppsMyModule config app loaded')
        import modules.apps_my_module.signals  # NOQA

        from modules.apps_my_module.tasks.scheduler import add_scheduler_tasks
        add_scheduler_tasks()
