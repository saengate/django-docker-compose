from django.dispatch import receiver
from django.db.models.signals import post_save

from apps_my_module.models import RecurringPayment
from apps_my_module.tasks.recurring_payment_task import DocumentGenerator


@receiver(
    post_save,
    sender=RecurringPayment,
    dispatch_uid='recurring_payment_created',
)
def recurring_payment_created(sender, instance, created, *args, **kwargs):
    DocumentGenerator().generate([instance])
