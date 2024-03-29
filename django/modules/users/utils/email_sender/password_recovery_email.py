from django.conf import settings

from modules.utils.services.sendgrid_client import SendGridClient
from modules.users.utils.email_sender.exceptions import EmailSenderException
from modules.users.models import User
from modules.users.utils.email_sender.exceptions import EmailSenderException


class PasswordRecoveryEmail(SendGridClient):

    def __init__(self) -> None:
        category = settings.SENDGRID_CATEGORIES['PASSWORD_RECOVERY']
        template_id = settings.FORGOT_PASSWORD_TEMPLATE
        self.from_address = settings.NO_REPLY_EMAIL_ADDRESS
        super().__init__(category=category, template_id=template_id)

    def send(self, user: User, **kwargs):
        receiver = {
            'name': user.first_name,
            'email': user.email,
        }
        try:
            return super().send(
                from_addr=self.from_address,
                receivers=[receiver],
                **kwargs,
            )
        except EmailSenderException as e:
            raise EmailSenderException() from e
