from django_filters import FilterSet

from task_manager.tasks.models import Task


class TaskFilter(FilterSet):
    class Meta:
        model = Task
        # Значение данного поля ни на что не влияет, поэтому оставим его пустым
        # Но оно должно быть задано, иначе фильтр падает с ошибкой
        fields = []
