from unittest.mock import patch

from cforemoto.tests.views.view_base_test_case import ViewBaseTestCase


class TestAdminUserView(ViewBaseTestCase):

    def setUp(self):
        super().setUp()
        self.url_admin_user = '/admin/users/'

    def do_admin_base_user(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)

    def test_destroy_when_delete_user_not_exists_then_return_401(self):
        self.client.logout()

        response = self.do_delete(self.url_admin_user)
        self.assertEqual(response.status_code, 401)

    def test_destroy_when_get_user_admin_not_exists_then_return_405(self):
        self.do_admin_base_user()
        response = self.do_get(self.url_admin_user)
        self.assertEqual(response.status_code, 405)

    def test_destroy_when_get_user_not_exists_then_return_403(self):
        response = self.do_get(self.url_admin_user)
        self.assertEqual(response.status_code, 403)

    def test_destroy_when_not_params_then_return_400(self):
        self.do_admin_base_user()
        response = self.do_delete(self.url_admin_user)
        self.assertEqual(response.status_code, 400)

    def test_destroy_when_not_valid_rut_then_return_400(self):
        self.do_admin_base_user()
        body = {'company_rut': '123456789'}
        response = self.do_delete(self.url_admin_user, body)
        self.assertEqual(response.status_code, 400)
        self.assertIn('company_rut', response.data)

    def test_destroy_when_not_valid_email_then_return_400(self):
        self.do_admin_base_user()
        body = {'email': 'email.com'}
        response = self.do_delete(self.url_admin_user, body)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    @patch('cforemoto.views.admin.users_view.UserCompany.delete_data_company')
    @patch('cforemoto.views.admin.users_view.move_users_to_blacklist')
    def test_destroy_when_valid_rut_then_return_204(
        self,
        move_black_mock,
        delete_company_mock,
    ):
        self.create_secod_user()
        self.do_admin_base_user()
        body = {'company_rut': self.another_company.rut}

        response = self.do_delete(self.url_admin_user, body)
        self.assertEqual(response.status_code, 204)

        self.assertTrue(delete_company_mock.called)
        self.assertTrue(move_black_mock.called)
        move_black_mock.assert_called_once_with(self.another_company.users)

    @patch('cforemoto.views.admin.users_view.UserCompany.delete_data_company')
    @patch('cforemoto.views.admin.users_view.move_users_to_blacklist')
    def test_destroy_when_valid_email_then_return_204(
        self,
        move_black_mock,
        delete_company_mock,
    ):
        self.create_secod_user()
        self.do_admin_base_user()
        body = {'email': self.another_user.email}

        response = self.do_delete(self.url_admin_user, body)
        self.assertEqual(response.status_code, 204)

        self.assertTrue(delete_company_mock.called)
        self.assertTrue(move_black_mock.called)
        move_black_mock.assert_called_once_with(self.another_company.users)
