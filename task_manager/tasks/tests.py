from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from task_manager.tasks.models import Task
from task_manager.tests import TestCaseAdvanced


class TasksTest(TestCaseAdvanced):
    def assertTask(self, task: Task, task_data: dict):
        """Проверяет данные задач на равенство

        Args:
            task (TaskStTaskatus): данные задачи из базы
            task_data (dict): данные задачи из фикстуры
        """
        
        self.assertEqual(task.__str__(), task_data["name"])
        self.assertEqual(task.description, task_data["description"])
        self.assertEqual(task.status_id, task_data["status"])
        self.assertEqual(task.author_id, task_data["author"])
        self.assertEqual(task.executor_id, task_data["executor"])
        
    def test_index_page(self):
        """Проверяет доступность страницы со списком задач.
        И корректность списка.
        """
        # Имя урла страницы
        url_name = "tasks:index"
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name)
        
        # Запрос данных страницы со списком задач
        index_page_response = self.client.get(reverse(url_name))
        
        # Проверяем статус ответа
        self.assertEqual(index_page_response.status_code, 200)
        
        # Проверяем наличие данных в контексте шаблона
        self.assertIn("filter", index_page_response.context)
        task_list = index_page_response.context["filter"].qs

        # Получаем задачи из базы
        tasks = Task.objects.all()
        
        # Проверяем, что задачи из response 
        # совпадают с задачами из базы
        self.assertQuerySetEqual(
            task_list,
            tasks,
            ordered=False,
        )
    
    def test_create_page(self):
        """Проверяет доступность страницы создания задачи
        """
        # Имя урла страницы
        url_name = "tasks:create"
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name)
        
        # Делаем запрос к странице создания задачи
        create_page_response = self.client.get(reverse(url_name))
        
        # Проверяем доступность страницы
        self.assertEqual(create_page_response.status_code, 200)
        
    def test_create(self):
        """Проверяет корректность процесса создания задачи
        """
        # Авторизуемся под существующим пользователем
        self._login_exist_user()
        
        # Получаем данные новой задачи из фикстуры
        new_task_data = self.test_data["tasks"]["new"]
        
        # Отправляем запрос на создание новой задачи
        create_response = self.client.post(
            reverse("tasks:create"), new_task_data
        )

        # Проверяем, что мы были перенаправлены на страницу со списком задач
        self.assertRedirects(create_response, reverse("tasks:index"))
        
        # Получаем из базы данные созданной
        created_task = Task.objects.get(name=new_task_data["name"])
        
        # Сравниваем данные задачи из базы и исходные данные из фикстуры
        self.assertTask(created_task, new_task_data)
    
    def test_update_page(self):
        """Проверяет доступность страницы обновления задачи
        """
        # Получаем существующую задачу базы
        exist_task = Task.objects.get(name=self._exist_task["name"])
        
        # Имя урла страницы
        url_name = "tasks:update"
        # Параметры запроса
        args = [exist_task.pk]
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name, args)
                
        # Переходим на страницу обновления задачи
        update_get_response = self.client.get(
            reverse(url_name, args=args)
        )

        # Проверяем, что страница доступна
        self.assertEqual(update_get_response.status_code, 200)

    def test_update(self):
        """Проверяет корректность обновления задачи
        """
        # Авторизуемся под существующим пользователем
        self._login_exist_user()
        
        # Получаем существующую задачу из базы
        exist_task = Task.objects.get(name=self._exist_task["name"])
        
        # Новые данные задачи
        updated_task_data = self._exist_task | {
            "description": "Новое описание задачи", 
        }
        
        # Обновляем данные задачи
        update_response = self.client.post(
            reverse("tasks:update", args=[exist_task.pk]),
            updated_task_data,
        )
        
        # Проверяем, что мы были перенаправлены 
        # на страницу со списком задач
        self.assertRedirects(update_response, reverse("tasks:index"))
        
        # Получаем из базы обновленную задачу
        updated_task = Task.objects.get(id=exist_task.pk)
        
        # Сравниваем данные обновленной задачи из базы 
        # и те, которые отправляли в запрос на обновление
        self.assertTask(updated_task, updated_task_data)
        
    def test_unavailability_delete_page(self):
        """Проверяет недоступность страницы удаления задачи для пользователя,
        который не является ее создателем.
        """
        # Получаем существующую задачу базы
        exist_task = Task.objects.get(name=self._exist_task["name"])
        
        # Имя урла страницы
        url_name = "tasks:delete"
        # Параметры запроса
        args = [exist_task.pk]
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        # Мы здесь логинимся под пользователем, который не создавал задач
        self._check_unavailability_request_and_login(url_name, args)
        
        # Заходим на страницу подтверждения удаления
        delete_page_response = self.client.get(
            reverse(url_name, args=args)
        )
        
        # Проверяем, что мы были перенаправлены 
        # обратно на страницу со списком задач
        self.assertRedirects(delete_page_response, reverse("tasks:index"))
        
    def test_availability_delete_page(self):
        """Проверяет доступность страницы удаления задачи для пользователя,
        который является ее создателем.
        """
        # Получаем существующую задачу базы
        exist_task = Task.objects.get(name=self._exist_task["name"])
        
        # Имя урла страницы
        url_name = "tasks:delete"
        # Параметры запроса
        args = [exist_task.pk]
        
        # Логинимся под пользователем, который создавал данную задачу
        self._login_exist_user_with_tasks()
        
        # Заходим на страницу подтверждения удаления
        delete_page_response = self.client.get(
            reverse(url_name, args=args)
        )
        
        # Проверяем доступность страницы
        self.assertEqual(delete_page_response.status_code, 200)
        
    def test_delete(self):
        """Проверяет корректность процесса удаления задачи
        """
        # Авторизуемся под пользователем, у которого есть задачи
        self._login_exist_user_with_tasks()
        
        # Получаем существуюущую задачу из базы
        exist_task = Task.objects.get(name=self._exist_task["name"])
        
        # Делаем запрос на удаление задачи
        delete_response = self.client.post(
            reverse("tasks:delete", args=[exist_task.pk])
        )
        
        # Проверяем, что мы были перенаправлены 
        # на страницу со списком задач
        self.assertRedirects(delete_response, reverse("tasks:index"))
        
        # Проверяем, что задачи нет в базе
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(name=self._exist_task["name"])
    
    def test_detail_page(self):
        """Проверяет доступность страницы просмотра задачи
        """
        # Получаем существующую задачу базы
        exist_task = Task.objects.get(name=self._exist_task["name"])
        
        # Имя урла страницы
        url_name = "tasks:detail"
        # Параметры запроса
        args = [exist_task.pk]
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name, args)
                
        # Переходим на страницу просмотра задачи
        detail_get_response = self.client.get(
            reverse(url_name, args=args)
        )

        # Проверяем, что страница доступна
        self.assertEqual(detail_get_response.status_code, 200)
