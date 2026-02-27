
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.tests import TestCaseAdvanced


class LabelsTest(TestCaseAdvanced):
    def assertLabel(self, label: Label, label_data: dict):
        """Проверяет данные меток на равенство

        Args:
            label (Label): данные метки из базы
            label_data (dict): данные метки из фикстуры
        """
        self.assertEqual(label.__str__(), label_data["name"])
    
    def test_index_page(self):
        """Проверяет доступность страницы со списком меток.
        И корректность списка.
        """
        # Имя урла страницы
        url_name = "labels:index"
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name)
        
        # Запрос данных страницы со списком меток
        index_page_response = self.client.get(reverse(url_name))
        
        # Проверяем статус ответа
        self.assertEqual(index_page_response.status_code, 200)
        
        # Проверяем наличие данных в контексте шаблона
        self.assertIn("label_list", index_page_response.context)
        label_list = index_page_response.context["label_list"]

        # Получаем метки из базы
        labels = Label.objects.all()
        
        # Проверяем, что метки из response 
        # совпадают со метками из базы
        self.assertQuerySetEqual(
            label_list,
            labels,
            ordered=False,
        )
    
    def test_create_page(self):
        """Проверяет доступность страницы создания метки
        """
        # Имя урла страницы
        url_name = "labels:create"
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name)
        
        # Делаем запрос к странице создания vtnrb
        create_page_response = self.client.get(reverse(url_name))
        
        # Проверяем доступность страницы
        self.assertEqual(create_page_response.status_code, 200)
        
    def test_create(self):
        """Проверяет корректность процесса создания метки
        """
        # Авторизуемся под существующим пользователем
        self._login_exist_user()
        
        # Получаем данные новой метки из фикстуры
        new_label_data = self.test_data["labels"]["new"]
        
        # Отправляем запрос на создание новой метки
        create_response = self.client.post(
            reverse("labels:create"), new_label_data
        )

        # Проверяем, что мы были перенаправлены на страницу со списком меток
        self.assertRedirects(create_response, reverse("labels:index"))
        
        # Получаем из базы данные созданной метки
        created_label = Label.objects.get(name=new_label_data["name"])
        
        # Сравниваем данные метки из базы и исходные данные из фикстуры
        self.assertLabel(created_label, new_label_data)
    
    def test_update_page(self):
        """Проверяет доступность страницы обновления метки
        """
        # Получаем существующую метку из базы
        exist_label = Label.objects.get(name=self._exist_label["name"])
        
        # Имя урла страницы
        url_name = "labels:update"
        # Параметры запроса
        args = [exist_label.pk]
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name, args)
                
        # Переходим на страницу обновления метки
        update_get_response = self.client.get(
            reverse(url_name, args=args)
        )

        # Проверяем, что страница доступна
        self.assertEqual(update_get_response.status_code, 200)

    def test_update(self):
        """Проверяет корректность обновления метки
        """
        # Авторизуемся под существующим пользователем
        self._login_exist_user()
        
        # Получаем существующую метку из базы
        exist_label = Label.objects.get(name=self._exist_label["name"])
        
        # Новые данные метки
        updated_label_data = self._exist_label | {
            "name": "duplicate-new", 
        }
        
        # Обновляем данные метки
        update_response = self.client.post(
            reverse("labels:update", args=[exist_label.pk]),
            updated_label_data,
        )
        
        # Проверяем, что мы были перенаправлены 
        # на страницу со списком меток
        self.assertRedirects(update_response, reverse("labels:index"))
        
        # Получаем из базы обновленную метку
        updated_label = Label.objects.get(id=exist_label.pk)
        
        # Сравниваем данные обновленной метки из базы 
        # и те, которые отправляли в запрос на обновление
        self.assertLabel(updated_label, updated_label_data)
        
    def test_delete_page(self):
        """Проверяет доступность страницы удаления метки
        """
        # Получаем существующую метку из базы
        exist_label = Label.objects.get(name=self._exist_label["name"])
        
        # Имя урла страницы
        url_name = "labels:delete"
        # Параметры запроса
        args = [exist_label.pk]
        
        # Проверим недоступность для незалогиненного пользователя и залогинимся
        self._check_unavailability_request_and_login(url_name, args)
        
        # Заходим на страницу подтверждения удаления
        delete_page_response = self.client.get(
            reverse(url_name, args=args)
        )
        
        # Проверяем, что страница доступна
        self.assertEqual(delete_page_response.status_code, 200)
        
    def test_delete_label_free_task(self):
        """Проверяет корректность процесса удаления метки,
        которая не привязана к задачам
        """
        # Авторизуемся под существующим пользователем
        self._login_exist_user()
        
        # Получаем существующую метку из базы
        exist_label = Label.objects.get(name=self._exist_label["name"])
        
        # Делаем запрос на удаление метки
        delete_response = self.client.post(
            reverse("labels:delete", args=[exist_label.pk])
        )
        
        # Проверяем, что мы были перенаправлены 
        # на страницу со списком меток
        self.assertRedirects(delete_response, reverse("labels:index"))
        
        # Проверяем, что метки нет в базе
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(name=self._exist_label["name"])
    
    def test_delete_label_related_task(self):
        """Проверяет корректность процесса удаления метки,
        которая привязана к задаче
        """
        # Авторизуемся под существующим пользователем
        self._login_exist_user()
        
        # Данные метки из фикстуры
        label_data = self.test_data["labels"]["existing_related_task"]
        
        # Получаем метку из базы
        label = Label.objects.get(name=label_data["name"])
        
        # Делаем запрос на удаление метки
        delete_response = self.client.post(
            reverse("labels:delete", args=[label.pk])
        )
        
        # Проверяем, что мы были перенаправлены 
        # на страницу со списком меток
        self.assertRedirects(delete_response, reverse("labels:index"))
        
        # Проверяем, что метка по прежнему есть в базе
        label = Label.objects.get(name=label_data["name"])
        self.assertLabel(label, label_data)
