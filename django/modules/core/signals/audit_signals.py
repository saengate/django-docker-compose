from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    post_delete,
)

from modules.core.models import CreationModificationDateBase


@receiver(
    post_save,
    sender=CreationModificationDateBase,
    dispatch_uid='audit_actions_save',
)
@receiver(
    post_delete,
    sender=CreationModificationDateBase,
    dispatch_uid='audit_actions_delete',
)
def add_actions_user_in_models(sender, instance, created, *args, **kwargs):
    # Your code here
    pass
