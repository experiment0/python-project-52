from django.forms import ModelForm, Textarea

from task_manager.tasks.models import Task


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        widgets = {
          'description': Textarea(attrs={'rows': 3, 'cols': 40}),
        }
