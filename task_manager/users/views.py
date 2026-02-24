from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    ListView,
    DeleteView,
    # DetailView,
    UpdateView,
)

from task_manager.users.forms import (
    UserCreationAdvancedForm,
    UserUpdateAdvancedForm,
)


class IndexView(ListView):
    model = User
    template_name = "users/index.html"


class UserCreate(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreationAdvancedForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("The user has been successfully registered.")


class PermissionRequiredAdvancedMixin(PermissionRequiredMixin):
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
                _("You do not have permission to modify another user.")
            )
            
            return HttpResponseRedirect(
                resolve_url("users:index")
            )
    
    def has_permission(self):
        auth_username = self.request.user
        target_user_id = self.kwargs['pk']
        target_user = User.objects.get(id=int(target_user_id))
        
        return auth_username == target_user
        

class UserUpdate(PermissionRequiredAdvancedMixin, UpdateView):
    model = User
    form_class = UserUpdateAdvancedForm
    template_name = "users/update.html"
    login_url = reverse_lazy("login")
    redirect_field_name = None
    
    def get_success_url(self):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            _("User successfully changed")
        )
        
        return reverse_lazy("users:index")


class UserDelete(PermissionRequiredAdvancedMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    login_url = reverse_lazy("login")
    redirect_field_name = None
    
    def get_success_url(self):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            _("The user has been successfully deleted.")
        )
        
        return reverse_lazy("users:index")
    