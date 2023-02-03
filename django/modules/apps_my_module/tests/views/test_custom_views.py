from rest_framework.test import (
    APIClient,
    APITestCase,
)


class TestCustomView(APITestCase):

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.url = '/custom/hello_world/'
        # self.url = reverse('custom_views')

    def test_hello_world_when_ok_then_return_200(self):
        output = self.client.get(self.url)

        self.assertEqual(output.status_code, 200)

        expect = {'message': 'Hello, world!'}
        self.assertDictEqual(
            expect,
            output.data,
        )

    def test_hello_world_when_post_then_return_200(self):
        data = {'name': 'prueba'}
        output = self.client.post(self.url, body=data, format='json')

        self.assertEqual(output.status_code, 200)

        data.update(
            {'custom_value': 18},
        )
        expect = {'message': data}
        self.assertDictEqual(
            expect,
            output.data,
        )
