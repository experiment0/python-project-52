from django.test import TestCase
from django.urls import reverse


class AppTest(TestCase):
    def test_index_page(self):
        """Проверяет доступность главной страницы
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """Проверяет доступность страницы входа
        """
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)