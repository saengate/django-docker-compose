from django.utils.translation import gettext_lazy as _
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.core'
    verbose_name = _('CoreModule')

    def ready(self):
        import modules.core.signals  # NOQA
        logger.info('CoreModule config app loaded')
