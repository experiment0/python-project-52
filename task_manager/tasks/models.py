from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.models import TimestampedModel
from task_manager.statuses.models import TaskStatus


class Task(TimestampedModel):
    name = models.CharField(
        _("name"), max_length=150, unique=True, null=False, blank=False
    )
    description = models.TextField(_("description"), null=True, blank=True)
    status = models.ForeignKey(
        TaskStatus, 
        on_delete=models.RESTRICT, 
        null=False, 
        blank=False,
        verbose_name=_("status"),
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT, 
        null=False,
        blank=False,
        related_name="created_tasks",
        verbose_name=_("author"),
    )
    executor = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        verbose_name=_("executor"),
    )
    labels = models.ManyToManyField(
        Label, 
        blank=True,
        db_constraint=True,
        verbose_name=_("labels"),
    )

    def __str__(self):
        return self.name
