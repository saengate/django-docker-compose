from modules.apps_my_module.tests.views.view_base_test_case import (
    ViewBaseTestCase,
)


class TestBlogView(ViewBaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/blog/'

    def test_get_when_all_ok_then_return_200(self):
        output = self.client.get(self.url)

        self.assertEqual(200, output.status_code)
