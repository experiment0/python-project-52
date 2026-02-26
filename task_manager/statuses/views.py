from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import RestrictedError
from django.http import HttpResponseRedirect
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
from task_manager.views import LoginRequiredMixinWithMessage


class IndexView(LoginRequiredMixinWithMessage, ListView):
    model = TaskStatus
    template_name = "statuses/index.html"
    
    
class TaskStatusCreate(
    LoginRequiredMixinWithMessage, SuccessMessageMixin, CreateView
):
    model = TaskStatus
    form_class = TaskStatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:index")
    success_message = _("Status successfully created")


class TaskStatusUpdate(
    LoginRequiredMixinWithMessage, SuccessMessageMixin, UpdateView
):
    model = TaskStatus
    form_class = TaskStatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:index")
    success_message = _("Status changed successfully")


class TaskStatusDelete(
    LoginRequiredMixinWithMessage, DeleteView
):
    model = TaskStatus
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:index")
    
    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.add_message(
                self.request, 
                messages.SUCCESS,
                _("Status successfully deleted")
            )
        except RestrictedError:
            messages.add_message(
                self.request, 
                messages.ERROR,
                _("The status cannot be deleted because it is in use.")
            )
        return HttpResponseRedirect(success_url)
