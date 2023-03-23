import json

from apps_my_module.tests.views.view_base_test_case import ViewBaseTestCase
from apps_my_module.tests.factories import EntryFactory


class TestEntryView(ViewBaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/entry/'

    def settings(self):
        self.entry_factory = EntryFactory()
        self.entry_instance = self.entry_factory.create()

    def test_get_when_user_not_login_then_return_401(self):
        self.client.logout()
        output = self.client.get(self.url)

        self.assertEqual(401, output.status_code)

    def test_get_when_user_login_then_return_200(self):
        output = self.client.get(self.url)

        self.assertEqual(200, output.status_code)

    def test_get_when_user_login_then_return_200_data(self):
        self.settings()
        output = self.client.get(self.url)

        self.assertEqual(200, output.status_code)

        data = output.json()
        data[0]['authors']
        data[0]['blog']
        self.entry_factory.blog_factory
        """ self.assertDictEqual(
            data[0]['blog']
        ) """

    def tests_post_create_entry_when_data_fail_then_raise_400(self):
        data = {
            '': '',
        }
        output = self.client.post(self.url, data=data)

        self.assertEqual(400, output.status_code)

    def tests_post_create_entry_when_data_fail_then_raise_201(self):
        data = {
            '': '',
        }
        output = self.client.post(self.url, data=data)

        self.assertEqual(201, output.status_code)
