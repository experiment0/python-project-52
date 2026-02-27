from django.contrib.auth.models import User
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import TaskStatus
from task_manager.tests import TestCaseAdvanced
from task_manager.utils import get_fixture_data


class TaskFilterTest(TestCaseAdvanced):
    def __init__(self, methodName: str = "runTest") -> None:
        self.tasks_data = get_fixture_data("tasks.json")
        super().__init__(methodName)
        
    def test_filtering_by_status(self):
        """Проверяет корректность фильтрации по полю status
        """
        # Залогинимся под пользователем, у которого есть задачи
        self._login_exist_user_with_tasks()
        
        # Данные статуса, привязанного к задачам
        status_name = \
            self.test_data["statuses"]["existing_related_task"]["name"]
        status = TaskStatus.objects.get(name=status_name)
        
        # Включаем в ссылку query параметр status
        response = self.client.get(
            reverse("tasks:index"), 
            {"status": status.pk}
        )
        
        # Проверяем, что в контексте есть задачи и получаем их
        self.assertIn("tasks", response.context)
        filtered_tasks = response.context["tasks"]
        
        # Вынимаем данные задач с проверяемым статусом из фикстур
        tasks_data_with_status = [
            task["fields"] for task in self.tasks_data 
                if task["fields"]["status"] == status.pk
        ]
        
        # Проверяем, что совпадает количество
        self.assertEqual(filtered_tasks.count(), len(tasks_data_with_status))
        
        # Проверяем, что на странице есть имена всех задач
        for task_data in tasks_data_with_status:
            self.assertContains(response, task_data["name"])

    def test_filtering_by_labels(self):
        """Проверяет корректность фильтрации по полю labels
        """
        # Залогинимся под пользователем, у которого есть задачи
        self._login_exist_user_with_tasks()
        
        # Данные метки, привязанной к задачам
        label_name = self.test_data["labels"]["existing_related_task"]["name"]
        label = Label.objects.get(name=label_name)
        
        # Включаем в ссылку query параметр labels
        response = self.client.get(
            reverse("tasks:index"), 
            {"labels": label.pk}
        )
        
        # Проверяем, что в контексте есть задачи и получаем их
        self.assertIn("tasks", response.context)
        filtered_tasks = response.context["tasks"]
        
        # Вынимаем данные задач с проверяемой меткой из фикстур
        tasks_data_with_label = [
            task["fields"] for task in self.tasks_data 
                if label.pk in task["fields"]["labels"]
        ]
        
        # Проверяем, что совпадает количество
        self.assertEqual(filtered_tasks.count(), len(tasks_data_with_label))
        
        # Проверяем, что на странице есть имена всех задач
        for task_data in tasks_data_with_label:
            self.assertContains(response, task_data["name"])
    
    def test_filtering_by_executor(self):
        """Проверяет корректность фильтрации по полю executor
        """
        # Залогинимся под пользователем, у которого есть задачи
        self._login_exist_user_with_tasks()
        
        # Получаем данные пользователя 
        user_data = self.test_data["users"]["existing_with_tasks"]
        user = User.objects.get(username=user_data["username"])
        
        # Включаем в ссылку query параметр executor
        response = self.client.get(
            reverse("tasks:index"), 
            {"executor": user.pk}
        )
        
        # Проверяем, что в контексте есть задачи и получаем их
        self.assertIn("tasks", response.context)
        filtered_tasks = response.context["tasks"]
        
        # Вынимаем данные задач с проверяемым значением executor из фикстур
        tasks_data_with_executor = [
            task["fields"] for task in self.tasks_data 
                if task["fields"]["executor"] == user.pk
        ]
        
        # Проверяем, что совпадает количество
        self.assertEqual(filtered_tasks.count(), len(tasks_data_with_executor))
        
        # Проверяем, что на странице есть имена всех задач
        for task_data in tasks_data_with_executor:
            self.assertContains(response, task_data["name"])
        
    def test_filtering_by_own_tasks(self):
        # Залогинимся под пользователем, у которого есть задачи
        self._login_exist_user_with_tasks()
        
        # Получаем данные пользователя 
        user_data = self.test_data["users"]["existing_with_tasks"]
        user = User.objects.get(username=user_data["username"])
        
        # Включаем в ссылку query параметр is_own_tasks
        response = self.client.get(
            reverse("tasks:index"), 
            {"is_own_tasks": "on"}
        )
        
        # Проверяем, что в контексте есть задачи и получаем их
        self.assertIn("tasks", response.context)
        filtered_tasks = response.context["tasks"]
        
        # Вынимаем данные задач с проверяемым значением author из фикстур
        tasks_data_by_author = [
            task["fields"] for task in self.tasks_data 
                if task["fields"]["author"] == user.pk
        ]
        
        # Проверяем, что совпадает количество
        self.assertEqual(filtered_tasks.count(), len(tasks_data_by_author))
        
        # Проверяем, что на странице есть имена всех задач
        for task_data in tasks_data_by_author:
            self.assertContains(response, task_data["name"])
