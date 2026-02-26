from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.models import TimestampedModel


class TaskStatus(TimestampedModel):
    name = models.CharField(
        _('name'), 
        max_length=100, 
        unique=True, 
        null=False,
        blank=False,
    )
    
    def __str__(self):
        return self.name
