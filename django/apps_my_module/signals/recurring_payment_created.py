from django.dispatch import receiver
from django.db.models.signals import post_save

from cforemoto.models import RecurringPayment
from cforemoto.tasks.recurring_payment_task import DocumentGenerator


@receiver(
    post_save,
    sender=RecurringPayment,
    dispatch_uid='recurring_payment_created',
)
def recurring_payment_created(sender, instance, created, *args, **kwargs):
    DocumentGenerator().generate([instance])
