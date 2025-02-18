from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        """Предустановка фикстур"""

        self.guest_client = Client()

    def test_homepage(self):
        """Проверка статуса главной страницы"""

        guest_client = Client()
        response = guest_client.get('/')
        self.assertEqual(response.status_code, 200)