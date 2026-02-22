from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    # DeleteView,
    # DetailView,
    # ListView,
    # UpdateView,
)

from task_manager.users.forms import UserCreationAdvancedForm


# Create your views here.
class UserCreate(CreateView):
    model = User
    form_class = UserCreationAdvancedForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
