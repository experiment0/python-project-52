from django.db.models import RestrictedError
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from task_manager.labels.models import Label


@receiver(pre_delete, sender=Label)  
def label_delete_handler(
    sender,  # класс модели
    instance,  # экземпляр, который удаляется
    **kwargs
):  
    if instance.task_set.exists():
        raise RestrictedError(
            "The label cannot be deleted because it is in use.", 
            set(instance.task_set.all())
        )
