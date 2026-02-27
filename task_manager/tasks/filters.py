from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(FilterSet):
    labels = ModelChoiceFilter(
        label=_('Label'),
        queryset=Label.objects.all(),
    )
    
    is_own_tasks = BooleanFilter(
        label=_("Only own tasks"),
        method="get_own_tasks",
        widget=forms.CheckboxInput,
    )
    
    def get_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset
    
    class Meta:
        model = Task
        fields = ["status", "executor"]
