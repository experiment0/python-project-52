from django.contrib.auth.models import User
from django.forms import ModelForm

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        
        self.fields["executor"].queryset = User.objects.all()
        self.fields["executor"].label_from_instance = \
            lambda obj: obj.get_full_name()
        
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]

