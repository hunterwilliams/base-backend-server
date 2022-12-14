from django.apps import AppConfig


class UserManagerConfig(AppConfig):
    name = "user_manager"
    verbose_name = "User Manager"

    def ready(self):
        import user_manager.signals
