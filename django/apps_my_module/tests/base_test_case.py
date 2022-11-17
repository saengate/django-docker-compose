import logging
from unittest.mock import patch

from django.test import TestCase


class BaseTestCase(TestCase):

    @classmethod
    def setupClass(cls):
        logging.disable(logging.CRITICAL)

    def setUp(self):
        self.confirmation_email_mock = self.create_mock_patch(
            'cforemoto.use_cases.email_sender.UserConfirmationEmail.send',
        )
        self.password_recovery_email_mock = self.create_mock_patch(
            'cforemoto.use_cases.email_sender.PasswordRecoveryEmail.send',
        )

    def create_mock_patch(self, module_path: str):
        patcher = patch(module_path)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing
