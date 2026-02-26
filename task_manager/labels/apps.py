from django.apps import AppConfig


class LabelsConfig(AppConfig):
    name = 'task_manager.labels'
    
    def ready(self):
        # Импортируем сигналы, чтобы они были зарегистрированы
        import task_manager.labels.signals  # noqa: F401
        pass
