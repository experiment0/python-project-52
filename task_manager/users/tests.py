from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from task_manager.tests import TestCaseAdvanced


class UsersTest(TestCaseAdvanced):        
    def assertUser(self, user: User, user_data: dict):
        """Проверяет данные пользователей на равенство

        Args:
            user (User): данные пользователя из базы
            user_data (dict): данные пользователя из фикстуры
        """
        self.assertEqual(user.__str__(), user_data["username"])
        self.assertEqual(user.first_name, user_data["first_name"])
        self.assertEqual(user.last_name, user_data["last_name"])
        
    def test_index_page(self):
        """Проверяет доступность страницы со списком пользователей.
        И корректность списка.
        """
        # Запрос данных страницы со списком пользователей
        index_page_response = self.client.get(reverse("users:index"))
        
        # Проверяем статус ответа
        self.assertEqual(index_page_response.status_code, 200)
        
        # Проверяем наличие данных в контексте шаблона
        self.assertIn("user_list", index_page_response.context)
        user_list = index_page_response.context["user_list"]

        # Получаем пользователей из базы
        users = User.objects.all()
        
        # Проверяем, что пользователи из response 
        # совпадают с пользователями из базы
        self.assertQuerySetEqual(
            user_list,
            users,
            ordered=False,
        )
    
    def test_create_page(self):
        """Проверяет доступность страницы создания пользователя (регистрации)
        """
        create_page_response = self.client.get(reverse("users:create"))
        self.assertEqual(create_page_response.status_code, 200)
        
    def test_create(self):
        """Проверяет корректность процесса создания пользователя (регистрации)
        """
        # Получаем данные нового пользователя из фикстуры
        new_user_data = self.test_data["users"]["new"]
        
        # Отправляем запрос на создание нового пользователя
        create_response = self.client.post(
            reverse("users:create"), new_user_data
        )

        # Проверяем, что мы были перенаправлены на страницу входа
        self.assertRedirects(create_response, reverse("login"))
        
        # Получаем из базы данные созданного пользователя
        created_user = User.objects.get(username=new_user_data["username"])
        
        # Сравниваем данные пользователя из базы и исходные данные из фикстуры
        self.assertUser(created_user, new_user_data)
    
    def test_update_page(self):
        """Проверяет доступность страницы обновления пользователя
        """
        # Получаем существующего пользователя из базы
        exist_user = User.objects.get(username=self._exist_user["username"])
        
        # Имя урла страницы
        url_name = "users:update"
        # Параметры запроса
        args = [exist_user.pk]
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name, args)
               
        # Переходим на страницу обновления пользователя
        update_get_response = self.client.get(
            reverse(url_name, args=args)
        )

        # Проверяем, что страница доступна
        self.assertEqual(update_get_response.status_code, 200)

    def test_update(self):
        """Проверяет корректность обновления пользователя
        """
        # Получаем существующего пользователя из базы
        exist_user = User.objects.get(username=self._exist_user["username"])
        
        # Авторизуемся под данным пользователем
        self._login_exist_user()
        
        # Новые данные пользователя
        updated_user_data = self._exist_user | {
            "first_name": "Hello-2", 
            "last_name": "World-2",
        }
        
        # Обновляем данные пользователя
        update_response = self.client.post(
            reverse("users:update", args=[exist_user.pk]),
            updated_user_data,
        )
        
        # Проверяем, что мы были перенаправлены 
        # на страницу со списком пользователей
        self.assertRedirects(update_response, reverse("users:index"))
        
        # Получаем из базы обновленного пользователя
        updated_user = User.objects.get(username=self._exist_user["username"])
        
        # Сравниваем данные обновленного пользователя из базы 
        # и те, которые отправляли в запрос на обновление
        self.assertUser(updated_user, updated_user_data)
        
    def test_delete_page(self):
        """Проверяет доступность страницы удаления пользователя
        """
        # Получаем существующего пользователя из базы
        exist_user = User.objects.get(username=self._exist_user["username"])
        
        # Имя урла страницы
        url_name = "users:delete"
        # Параметры запроса
        args = [exist_user.pk]
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name, args)
        
        # Заходим на страницу подтверждения удаления
        delete_page_response = self.client.get(
            reverse(url_name, args=args)
        )
        
        # Проверяем, что страница доступна
        self.assertEqual(delete_page_response.status_code, 200)
        
    def test_delete(self):
        """Проверяет корректность процесса удаления пользователя
        """
        # Получаем существующего пользователя из базы
        exist_user = User.objects.get(username=self._exist_user["username"])
        
        # Авторизуемся под данным пользователем
        self._login_exist_user()
        
        # Делаем запрос на удаление пользователя
        delete_response = self.client.post(
            reverse("users:delete", args=[exist_user.pk])
        )
        
        # Проверяем, что мы были перенаправлены 
        # на страницу со списком пользователей
        self.assertRedirects(delete_response, reverse("users:index"))
        
        # Проверяем, что пользователя нет в базе
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=self._exist_user["username"])
