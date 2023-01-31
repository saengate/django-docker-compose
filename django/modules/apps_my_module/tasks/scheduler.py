import logging
import django_rq
from rq.registry import (
    ScheduledJobRegistry,
    clean_registries,
)

from modules.utils.date_utils import DateUtils


logger = logging.getLogger(__name__)


def add_scheduler_tasks():
    name_queue = 'default'
    queue = django_rq.get_queue(name_queue)
    registry = ScheduledJobRegistry(queue=queue)

    if registry.count > 0:
        registry.remove_jobs()
        registry.cleanup()
        clean_registries(queue)
        redis = django_rq.get_connection()
        redis.flushall()
        logger.warning('Clean all queues jobs!')

    scheduler = django_rq.get_scheduler(name_queue)

    """ new_task = scheduler.cron(
        '0 0 * * 1',
        func=CLASSTASK().start,
        args=[],
        kwargs={},
        repeat=None,
        queue_name='default',
        meta={},
        use_local_timezone=True,
    )
    registry.schedule(user_inactive, DateUtils().now())
    """

    logger.info(f'Enqueue {registry.count} jobs for apps!')
