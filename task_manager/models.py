from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    """Абстрактная модель с добавлением временных меток"""

    created_at = models.DateTimeField(_('created date'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated date'), auto_now=True)

    class Meta:
        abstract = True
