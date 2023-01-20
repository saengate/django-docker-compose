from unittest.mock import (
    MagicMock,
    patch,
)

from users.tests.views.view_base_test_case import ViewBaseTestCase
from users.tests.factories import (
    UserFactory,
)
from users.tasks.user_inactive import UserInactive
from utils.date_utils import DateUtils
from utils.string_utils import random_string


class TestUserInactive(ViewBaseTestCase):
    def setUp(self):
        super().setUp()
        last_login_date = DateUtils().create_aware(2019, 1, 1)
        self.user.last_login = last_login_date
        self.user.save()

    def test_task_scheduler_running_when_ok(self, detete_data_mock):
        detete_data_mock.return_value = MagicMock()
        UserInactive().start()

        self.assertTrue(detete_data_mock.called)

    def test_task_scheduler_running_when_no_inactive_users(
        self,
        detete_data_mock,
    ):
        last_login_date = DateUtils().today_datetime()
        self.user.last_login = DateUtils().make_aware(last_login_date)
        self.user.save()
        detete_data_mock.return_value = MagicMock()
        UserInactive().start()

        self.assertFalse(detete_data_mock.called)

    def test_task_scheduler_running_when_another_inactive_users(
        self,
        UserCompanyMock,
    ):
        UCMock = MagicMock()
        UCMock.delete_data_company.return_value = None
        UserCompanyMock.return_value = UCMock
        dateUtils = DateUtils()

        today = dateUtils.today_datetime()
        four_months_ago = dateUtils.rest_months_to_date(dateUtils.today(), 4)
        four_months_ago = dateUtils.date_to_datetime(four_months_ago)

        self.other_user = UserFactory().create()
        self.other_user.date_joined = four_months_ago
        self.other_user.save()

        self.user.last_login = today
        self.user.save()

        UserInactive().start()

        UserCompanyMock.assert_called_once_with(self.other_user.username)
        self.assertTrue(UCMock.delete_data_company.called)

    def test_task_scheduler_running_when_last_login_four_months_ago_no_companies(
        self,
        UserCompanyMock,
    ):
        UCMock = MagicMock()
        UCMock.delete_data_company.return_value = None
        UserCompanyMock.return_value = UCMock
        dateUtils = DateUtils()

        four_months_ago = dateUtils.rest_months_to_date(dateUtils.today(), 4)
        four_months_ago = dateUtils.date_to_datetime(four_months_ago)

        today = dateUtils.today_datetime()
        self.other_user = UserFactory().create()
        self.other_user.last_login = four_months_ago
        self.other_user.save()
        self.user.last_login = today
        self.user.save()

        UserInactive().start()

        UserCompanyMock.assert_called_once_with(self.other_user.username)
        self.assertTrue(UCMock.delete_data_company.called)
