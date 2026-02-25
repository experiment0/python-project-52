from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.views import LoginRequiredMixinWithMessage


class IndexView(LoginRequiredMixinWithMessage, ListView):
    model = Task
    template_name = "tasks/index.html"
  

class TaskDetail(LoginRequiredMixinWithMessage, DetailView):
    model = Task
    template_name = "tasks/detail.html"


class TaskCreate(
    LoginRequiredMixinWithMessage, SuccessMessageMixin, CreateView
):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:index")
    success_message = _("Task successfully created")
    
    def form_valid(self, form):
        # Перед валидацией формы устанавливаем автором задачи
        # текущего залогиненного пользователя
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdate(
    LoginRequiredMixinWithMessage, SuccessMessageMixin, UpdateView
):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:index")
    success_message = _("Task changed successfully")


class PermissionRequiredMixinForAuthorshipVerification(PermissionRequiredMixin):
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.add_message(
                self.request, 
                messages.ERROR,
                _("You are not logged in! Please log in.")
            )            
            return super().handle_no_permission()
        else:
            messages.add_message(
                self.request, 
                messages.ERROR,
                _("A task can only be deleted by its author.")
            )            
            return HttpResponseRedirect(
                resolve_url("tasks:index")
            )
    
    def has_permission(self):
        try:
            # id залогиненного пользователя
            auth_username_id = self.request.user.id
            
            # id задачи из параметров урла
            target_task_id = self.kwargs['pk']
            # Объект задачи, который собираются удалять
            target_task = Task.objects.get(id=int(target_task_id))
            # Проверяем, что id залогиненного пользователя 
            # и id автора задачи совпадают
            return auth_username_id == target_task.author_id
        
        # Конкретная ошибка, которую мы могли бы отловить - 
        # это self.model.DoesNotExist в случае, 
        # если задача с переданным id не существует.
        # Но родительский метод обработает ее корректно, 
        # поэтому не отлавливаем этот частный случай.
        except Exception:            
            return super().has_permission()
        

class TaskDelete(
    PermissionRequiredMixinForAuthorshipVerification, DeleteView
):
    # Список прав нужен, 
    # чтобы не падал вызов родительского метода has_permission.
    permission_required = ["tasks.delete_task"]
    model = Task
    template_name = "tasks/delete.html"
    login_url = reverse_lazy("login")
    redirect_field_name = None
    
    def get_success_url(self):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            _("The task was successfully deleted.")
        )        
        return reverse_lazy("tasks:index")
