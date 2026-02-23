from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    # DeleteView,
    # DetailView,
    # UpdateView,
    ListView,
)

from task_manager.users.forms import UserCreationAdvancedForm


class IndexView(ListView):
    model = User
    template_name = "users/index.html"


class UserCreate(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreationAdvancedForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("The user has been successfully registered.")
