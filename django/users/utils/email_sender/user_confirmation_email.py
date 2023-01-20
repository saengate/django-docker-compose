from django.conf import settings

from users.utils.email_sender.exceptions import EmailSenderException
from utils.services.sendgrid_client import SendGridClient


class UserConfirmationEmail(SendGridClient):

    def __init__(self) -> None:
        category = settings.SENDGRID_CATEGORIES['USER_CONFIRMATION']
        template_id = settings.USER_CONFIRMATION_TEMPLATE
        self.from_address = settings.NO_REPLY_EMAIL_ADDRESS
        super().__init__(category=category, template_id=template_id)

    def send(self, user, **kwargs):
        confirmation_url_pattern = '{}/users/confirm?verification_secret={}'
        confirmation_url = confirmation_url_pattern.format(
            settings.BACKEND_URL, user.verification_secret,
        )
        receiver = {
            'name': user.first_name,
            'email': user.email,
        }
        kwargs = {
            'confirmation_url': confirmation_url,
        }
        try:
            return super().send(
                from_addr=self.from_address,
                receivers=[receiver],
                **kwargs,
            )
        except EmailSenderException as e:
            raise e
