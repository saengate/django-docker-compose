import django.dispatch
from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_delete,
    pre_save,
)
from django.core.signals import request_finished

from modules.apps_my_module.models import Entry


@receiver(
    post_save,
    sender=Entry,
    dispatch_uid='when_entry_save',
)
def custom_signal(sender, instance, created, *args, **kwargs):
    pass


@receiver(
    request_finished,
    dispatch_uid='when_custom_request',
)
def my_callback(sender, **kwargs):
    pass


signal_done = django.dispatch.Signal()


@receiver(
    signal_done,
    dispatch_uid='when_custom_signal_class',
)
def another_call(sender, **kwargs):
    print("Prueba signal")


class SignalStore:
    def send_signal(self, *args):
        signal_done.send(sender=self.__class__, *args)
