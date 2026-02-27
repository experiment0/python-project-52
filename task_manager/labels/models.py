from django.db import models
from django.db.models import RestrictedError
from django.utils.translation import gettext_lazy as _

from task_manager.models import TimestampedModel


class Label(TimestampedModel):
    name = models.CharField(
        _('name'), 
        max_length=100, 
        unique=True, 
        null=False, 
        blank=False,
    )
    
    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.task_set.exists() > 0:
            raise RestrictedError(
                "The label cannot be deleted because it is in use.", 
                set(self.task_set.all())
            )
        else:
            super().delete(*args, **kwargs)
    