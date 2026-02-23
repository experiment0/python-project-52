from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class LoginAdvancedView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    
    def get_success_url(self):
        return reverse_lazy("index")
    
    success_message = _("You are logged in")


class LogoutAdvancedView(LogoutView):
    def get_success_url(self):
        messages.add_message(
            self.request, 
            messages.INFO,
            _("You are logged out")
        )
        
        return reverse_lazy("index")
