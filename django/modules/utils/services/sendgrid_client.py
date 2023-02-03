import logging

from typing import List
from django.conf import settings
from sendgrid import (
    SendGridAPIClient,
    MailSettings,
    SandBoxMode,
)
from sendgrid.helpers.mail import (
    Personalization,
    Mail,
    Email,
    Category,
)

from modules.utils.services.exceptions import EmailSenderClientException


logger = logging.getLogger(__name__)


class SendGridClient:

    def __init__(self, category: str, template_id: str = None):
        self.api_key = settings.SENDGRID_API_KEY
        self.sg_client = SendGridAPIClient(self.api_key)
        self.category = category
        self.template_id = template_id
        self.sandbox = False

    def _check_sandbox_mode(self, mail: Mail):
        if self.sandbox:
            mail_settings = MailSettings()
            mail_settings.sandbox_mode = SandBoxMode(True)
            mail.mail_settings = mail_settings

    def _send_email(self, mail: Mail, category: str):
        if category:
            mail.category = Category(category)
        try:
            response = self.sg_client.send(mail)
        except Exception as e:
            logger.exception('UNHANDLED SENDGRID EXCEPTION: %s', e)
            raise EmailSenderClientException() from e

        if response.status_code not in [200, 202]:
            logger.exception(
                'UNEXPECTED SENDGRID RESPONSE: %s', response.status_code,
            )
            raise EmailSenderClientException()
        return mail

    def send(self, from_addr, receivers, **kwargs) -> Mail:
        if self.template_id:
            return self.send_with_template(
                from_addr=from_addr,
                receivers=receivers,
                context=kwargs,
            )
        else:
            return self.send_with_message(
                from_addr=from_addr,
                to_addr=receivers,
                subject=kwargs.get('subject'),
                message=kwargs.get('message'),
            )

    def send_with_message(
        self,
        from_addr: str,
        to_addr: List[str],
        subject: str,
        message=None,
    ):
        mail = Mail(
            from_email=from_addr,
            to_emails=to_addr,
            subject=subject,
            html_content=message,
        )
        return self._send_email(mail, self.category)

    def send_with_template(
        self,
        from_addr: str,
        receivers: List[dict],
        context: dict = None,
    ):
        """
            Send a email using a sendgrid template
            :param str from_addr: The email address sending the message
            :param str receivers: A list of receivers (name - email - custom)
            :param dict context: Specific data needed into template and generic
            for all receivers (It could be included into receivers list too)
            :return: Sendgrid Mail instance
            :rtype: Mail
            :raises HttpError: if sendgrid API has an error
            :raises EmailSenderClientException: if the response code is not 200
        """
        context = context or dict()
        message = Mail(
            from_email=from_addr,
        )
        message.template_id = self.template_id

        for receiver in receivers:
            personalization = Personalization()
            personalization.add_to(Email(receiver['email'], receiver['name']))
            receiver.update(**context)
            personalization.dynamic_template_data = receiver
            message.add_personalization(personalization)

        self._check_sandbox_mode(message)
        return self._send_email(message, self.category)
