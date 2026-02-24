from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


class UserCreationAdvancedForm(UserCreationForm):
    first_name = forms.CharField(
        label=capfirst(_("first name")), 
        max_length=150, 
        required=True,
    )
    last_name = forms.CharField(
        label=capfirst(_("last name")), 
        max_length=150, 
        required=True,
    )
    
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "username", "password1", "password2",
        ]


class UserUpdateAdvancedForm(UserCreationAdvancedForm):
    def clean_username(self):
        username = self.cleaned_data.get("username")
        
        return username
