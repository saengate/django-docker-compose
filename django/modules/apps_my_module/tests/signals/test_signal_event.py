from unittest.mock import patch

from rest_framework.test import (
    APIClient,
    APITestCase,
)
from django.db.models import signals
from django.core.signals import request_finished

from modules.apps_my_module.models import Entry
from modules.apps_my_module.tests.factories import EntryFactory
from modules.apps_my_module.signals.signal_event import (
    SignalStore,
    custom_signal,
    signal_done,
)


class TestsSignals(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        signals.post_save.disconnect(
            sender=Entry,
            dispatch_uid='when_entry_save',
        )
        request_finished.disconnect(
            dispatch_uid='when_custom_request',
        )
        signal_done.disconnect(
            dispatch_uid='when_custom_signal_class'
        )

    def setUpAPI(self):
        self.client = APIClient()
        self.url = '/custom/hello_world/'

    def tearDown(self) -> None:
        super().tearDown()
        signals.post_save.connect(
            receiver=custom_signal,
            sender=Entry,
            dispatch_uid='when_entry_save',
        )
        request_finished.connect(
            request_finished,
            dispatch_uid='when_custom_request',
        )
        signal_done.connect(
            signal_done,
            dispatch_uid='when_custom_signal_class',
        )

    @patch(
        'modules.apps_my_module.signals.signal_event.custom_signal',
        autospec=True,
    )
    def test_entry_when_save_then_dispatch_signal(self, mock_signal):
        signals.post_save.connect(mock_signal)
        EntryFactory().create()

        mock_signal.assert_called()
        signals.post_save.disconnect(mock_signal)

    @patch(
        'modules.apps_my_module.signals.signal_event.my_callback',
        autospec=True,
    )
    def test_request_when_finish_then_dispatch_signal(self, mock_signal):
        self.setUpAPI()
        request_finished.connect(mock_signal)
        self.client.get(self.url)

        mock_signal.assert_called()
        request_finished.disconnect(mock_signal)
        self.assertLogs('Prueba middleware')

    @patch(
        'modules.apps_my_module.signals.signal_event.another_call',
        autospec=True,
    )
    def test_my_signal_when_send_then_dispatch_signal(self, mock_signal):
        signal_done.connect(mock_signal)
        SignalStore().send_signal()

        mock_signal.assert_called()
        signal_done.disconnect(mock_signal)
