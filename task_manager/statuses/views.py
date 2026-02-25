from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.statuses.forms import TaskStatusForm
from task_manager.statuses.models import TaskStatus


class LoginRequiredAdvancedMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")
    redirect_field_name = None
    
    def get_login_url(self):
        messages.add_message(
            self.request, 
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )        
        return super().get_login_url()


class IndexView(LoginRequiredAdvancedMixin, ListView):
    model = TaskStatus
    template_name = "statuses/index.html"
    
    
class TaskStatusCreate(
    LoginRequiredAdvancedMixin, SuccessMessageMixin, CreateView
):
    model = TaskStatus
    form_class = TaskStatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:index")
    success_message = _("Status successfully created")


class TaskStatusUpdate(
    LoginRequiredAdvancedMixin, SuccessMessageMixin, UpdateView
):
    model = TaskStatus
    form_class = TaskStatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:index")
    success_message = _("Status changed successfully")


# TODO - Статус нельзя удалить, если он связан хотя бы с одной задачей
class TaskStatusDelete(
    LoginRequiredAdvancedMixin, SuccessMessageMixin, DeleteView
):
    model = TaskStatus
    success_url = reverse_lazy("statuses:index")
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:index")
    success_message = _("Status successfully deleted")
