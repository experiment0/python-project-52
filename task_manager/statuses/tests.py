from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from task_manager.statuses.models import TaskStatus
from task_manager.tests import TestCaseAdvanced


class StatusesTest(TestCaseAdvanced):
    def assertStatus(self, status: TaskStatus, status_data: dict):
        """Проверяет данные статусов на равенство

        Args:
            status (TaskStatus): данные статуса из базы
            status_data (dict): данные статуса из фикстуры
        """
        self.assertEqual(status.__str__(), status_data["name"])
    
    def test_index_page(self):
        """Проверяет доступность страницы со списком статусов.
        И корректность списка.
        """
        # Имя урла страницы
        url_name = "statuses:index"
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name)
        
        # Запрос данных страницы со списком статусов
        index_page_response = self.client.get(reverse(url_name))
        
        # Проверяем статус ответа
        self.assertEqual(index_page_response.status_code, 200)
        
        # Проверяем наличие данных в контексте шаблона
        self.assertIn("taskstatus_list", index_page_response.context)
        status_list = index_page_response.context["taskstatus_list"]

        # Получаем статусы из базы
        statuses = TaskStatus.objects.all()
        
        # Проверяем, что статусы из response 
        # совпадают со статусами из базы
        self.assertQuerySetEqual(
            status_list,
            statuses,
            ordered=False,
        )
    
    def test_create_page(self):
        """Проверяет доступность страницы создания статуса
        """
        # Имя урла страницы
        url_name = "statuses:create"
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name)
        
        # Делаем запрос к странице создания статуса
        create_page_response = self.client.get(reverse(url_name))
        
        # Проверяем доступность страницы
        self.assertEqual(create_page_response.status_code, 200)
        
    def test_create(self):
        """Проверяет корректность процесса создания статуса
        """
        # Авторизуемся под существующим пользователем
        self._login_exist_user()
        
        # Получаем данные нового статуса из фикстуры
        new_status_data = self.test_data["statuses"]["new"]
        
        # Отправляем запрос на создание нового статуса
        create_response = self.client.post(
            reverse("statuses:create"), new_status_data
        )

        # Проверяем, что мы были перенаправлены на страницу со списком статусов
        self.assertRedirects(create_response, reverse("statuses:index"))
        
        # Получаем из базы данные созданного статуса
        created_status = TaskStatus.objects.get(name=new_status_data["name"])
        
        # Сравниваем данные статуса из базы и исходные данные из фикстуры
        self.assertStatus(created_status, new_status_data)
    
    def test_update_page(self):
        """Проверяет доступность страницы обновления статуса
        """
        # Получаем существующий статус из базы
        exist_status = TaskStatus.objects.get(name=self._exist_status["name"])
        
        # Имя урла страницы
        url_name = "statuses:update"
        # Параметры запроса
        args = [exist_status.pk]
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name, args)
                
        # Переходим на страницу обновления статуса
        update_get_response = self.client.get(
            reverse(url_name, args=args)
        )

        # Проверяем, что страница доступна
        self.assertEqual(update_get_response.status_code, 200)

    def test_update(self):
        """Проверяет корректность обновления статуса
        """
        # Авторизуемся под существующим пользователем
        self._login_exist_user()
        
        # Получаем существующий статус из базы
        exist_status = TaskStatus.objects.get(name=self._exist_status["name"])
        
        # Новые данные статуса
        updated_status_data = self._exist_status | {
            "name": "created-new", 
        }
        
        # Обновляем данные статуса
        update_response = self.client.post(
            reverse("statuses:update", args=[exist_status.pk]),
            updated_status_data,
        )
        
        # Проверяем, что мы были перенаправлены 
        # на страницу со списком статусов
        self.assertRedirects(update_response, reverse("statuses:index"))
        
        # Получаем из базы обновленный статус
        updated_status = TaskStatus.objects.get(id=exist_status.pk)
        
        # Сравниваем данные обновленного статуса из базы 
        # и те, которые отправляли в запрос на обновление
        self.assertStatus(updated_status, updated_status_data)
        
    def test_delete_page(self):
        """Проверяет доступность страницы удаления статуса
        """
        # Получаем существующий статус из базы
        exist_status = TaskStatus.objects.get(name=self._exist_status["name"])
        
        # Имя урла страницы
        url_name = "statuses:delete"
        # Параметры запроса
        args = [exist_status.pk]
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name, args)
        
        # Заходим на страницу подтверждения удаления
        delete_page_response = self.client.get(
            reverse(url_name, args=args)
        )
        
        # Проверяем, что страница доступна
        self.assertEqual(delete_page_response.status_code, 200)
        
    def test_delete(self):
        """Проверяет корректность процесса удаления статуса
        """
        # Авторизуемся под существующим пользователем
        self._login_exist_user()
        
        # Получаем существующий статус из базы
        exist_status = TaskStatus.objects.get(name=self._exist_status["name"])
        
        # Делаем запрос на удаление статуса
        delete_response = self.client.post(
            reverse("statuses:delete", args=[exist_status.pk])
        )
        
        # Проверяем, что мы были перенаправлены 
        # на страницу со списком статусов
        self.assertRedirects(delete_response, reverse("statuses:index"))
        
        # Проверяем, что статуса нет в базе
        with self.assertRaises(ObjectDoesNotExist):
            TaskStatus.objects.get(name=self._exist_status["name"])
