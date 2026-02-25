from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskStatus(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True, blank=False)
    created_at = models.DateTimeField(_('created date'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated date'), auto_now=True)
    
    def __str__(self):
        return self.name
