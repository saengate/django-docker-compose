from django.dispatch import receiver
from django.db.models.signals import post_save

from modules.apps_my_module.models import Model


@receiver(
    post_save,
    sender=Model,
    dispatch_uid='ID_KEY',
)
def recurring_payment_created(sender, instance, created, *args, **kwargs):
    # Your code here
    pass
