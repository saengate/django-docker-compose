import analytics
import logging

from django.conf import settings

from modules.users.models import User


logger = logging.getLogger(__name__)


class SegmentAnalytics:
    """ Send analytics data to Segment services """

    def __init__(self, user=None):
        self.user = self.__format_data_user(user)
        self.isTesterUser = self.__validate_is_tester_user()
        self.analytics = analytics
        self.analytics.write_key = settings.SEGMENT_WRITE_KEY

    @staticmethod
    def not_production():
        return settings.ENVIRONMENT != 'production'

    def __validate_is_tester_user(self):
        is_tester = SegmentAnalytics.not_production()
        if not is_tester:
            is_tester = getattr(self.user, 'is_tester', False)
        return is_tester

    def __format_data_user(self, user):
        if isinstance(user, dict):
            class Object(object):
                pass
            obj_user = Object()
            try:
                obj_user.id = user['id']
                obj_user.email = user['email']
                obj_user.is_tester = user['is_tester']
                obj_user.first_name = user['first_name']
                obj_user.last_name = user['last_name']
                obj_user.username = user['username']
                obj_user.companies = [
                    {
                        'rut': user['company_rut'],
                        'name': user['company_name'],
                    },
                ]
                user = obj_user
            except KeyError:
                logger.error("User not have all needed attributes to segment")
                user = None
        return user

    def identify(self):
        flag = False
        if self.isTesterUser is False and self.user:
            try:
                if isinstance(self.user, User):
                    companies = list(self.user.companies.all())[0].__dict__
                else:
                    company = dict(self.user.companies[0])
                    companies = {
                        'rut': company.get('rut'),
                        'name': company.get('name'),
                    }
            except (IndexError, AttributeError):
                logger.error(f"Cannot get company for user {self.user.id}")
                companies = {
                    'rut': None,
                    'name': None,
                }
            self.analytics.identify(
                self.user.id,
                {
                    'firstName': self.user.first_name,
                    'lastName': self.user.last_name,
                    'username': self.user.username,
                    'email': self.user.email,
                    'company': {
                        'rut': companies.get('rut'),
                        'name': companies.get('name'),
                    },
                },
            )
            flag = True
        return flag

    def receive_engagement_email(self, details: dict):
        flag = False
        if details.get('template') == settings.DOCS_NEAR_TO_EXPIRE_TEMPLATE:
            details['email_type'] = 'porVencer'
        elif details.get('template') == settings.DOCS_EXPIRE_DOCUMENTS_TEMPLATE:
            details['email_type'] = 'vencidos'
        if self.isTesterUser is False \
                and details.get('email_type') \
                and details.get('documents_quantity') \
                and self.user \
                and self.identify():
            self.analytics.track(
                self.user.id,
                "ReceiveEngagementEmail",
                {
                    "numberOfDocuments": details['documents_quantity'],
                    "emailType": details['email_type'],
                },
            )
            flag = True
        return flag
