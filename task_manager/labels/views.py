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

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.views import LoginRequiredMixinWithMessage


class IndexView(LoginRequiredMixinWithMessage, ListView):
    model = Label
    template_name = "labels/index.html"
    extra_context = {
        "title": _("Labels"),
    }
    

class LabelCreate(
    LoginRequiredMixinWithMessage, SuccessMessageMixin, CreateView
):
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:index")
    success_message = _("Label successfully created")
    extra_context = {
        "title": _("Create a label"),
    }


class LabelUpdate(
    LoginRequiredMixinWithMessage, SuccessMessageMixin, UpdateView
):
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:index")
    success_message = _("Label changed successfully")
    extra_context = {
        "title": _("Updating label"),
    }


class LabelDelete(
    LoginRequiredMixinWithMessage, DeleteView
):
    model = Label
    template_name = "layouts/confirm_delete.html"
    success_url = reverse_lazy("labels:index")
    extra_context = {
        "title": _("Deleting a label"),
    }
    
    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.add_message(
                self.request, 
                messages.SUCCESS,
                _("Label successfully deleted")
            )
        except RestrictedError:
            messages.add_message(
                self.request, 
                messages.ERROR,
                _("The label cannot be deleted because it is in use.")
            )
        return HttpResponseRedirect(success_url)
