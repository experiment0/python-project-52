from typing import Optional

from django.test import TestCase
from django.urls import reverse

from task_manager.utils import FixtureDataType, get_test_data


class TestCaseAdvanced(TestCase):
    """Класс содержит элементы, общие для всех тестов
    (общие фикстуры, аутентификацию пользователя)
    """
    
    # Указываем имена фикстур для загрузки в БД
    fixtures = ["users.json", "statuses.json", "tasks.json", "labels.json"]
    
    @classmethod
    def setUpTestData(cls):
        """Загружает тестовые данные
        """
        cls.test_data: FixtureDataType = get_test_data()
    
    @property
    def _exist_user(self) -> dict:
        """Возвращает из фикстуры данные существующего пользователя без задач.

        Returns:
            dict: данные существующего пользователя без задач
        """
        return self.test_data["users"]["existing_without_tasks"]
    
    @property
    def _exist_status(self) -> dict:
        """Возвращает из фикстуры данные существующего статуса, 
        не привязанного к задачам.

        Returns:
            dict: данные существующего статуса, не привязанного к задачам
        """
        return self.test_data["statuses"]["existing_free_task"]
    
    @property
    def _exist_label(self) -> dict:
        """Возвращает из фикстуры данные существующей метки, 
        не привязанной к задачам.

        Returns:
            dict: данные существующей метки, не привязанной к задачам
        """
        return self.test_data["labels"]["existing_free_task"]
    
    @property
    def _exist_task(self) -> dict:
        """Возвращает из фикстуры данные существующей задачи.

        Returns:
            dict: данные существующей задачи
        """
        return self.test_data["tasks"]["existing"]
        
    def _login_exist_user(self):
        """Выполняет авторизацию под данными существующего пользователя,
        у которого нет задач
        """
        # Делаем запрос на авторизацию
        login_response = self.client.post(
            reverse("login"), {
                "username": self._exist_user["username"],
                "password": self._exist_user["password1"],
            }
        )        
        # Проверяем, что мы были перенаправлены главную страницу
        self.assertRedirects(login_response, reverse("index"))
    
    def _login_exist_user_with_tasks(self):
        """Выполняет авторизацию под данными существующего пользователя,
        у которого есть задачи
        """
        # Пользователь, который создавал задачи
        user_with_tasks = self.test_data["users"]["existing_with_tasks"]
        # Делаем запрос на авторизацию
        login_response = self.client.post(
            reverse("login"), {
                "username": user_with_tasks["username"],
                "password": user_with_tasks["password1"],
            }
        )        
        # Проверяем, что мы были перенаправлены главную страницу
        self.assertRedirects(login_response, reverse("index"))
    
    def _check_unavailability_request_and_login(
        self, 
        url_name: str, 
        args: Optional[list] = None
    ):
        """Проверяет недоступность страницы для неавторизованного пользователя.
        И производит авторизацию.

        Args:
            url_name (str): имя урла
            args (Optional[list], optional): параметры запроса. 
                                            По умолчанию None.
        """
        # Делаем запрос 
        response = self.client.get(reverse(url_name, args=args))
        
        # Убержаемся, что нас переправили на страницу входа
        self.assertRedirects(response, reverse("login"))
        
        # Авторизуемся под существующим пользователем
        self._login_exist_user()


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
