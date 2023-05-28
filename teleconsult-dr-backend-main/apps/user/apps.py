from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UserConfig(AppConfig):
    name = 'apps.user'

    def ready(self):
        from apps.user.signals import create_admin

        post_migrate.connect(create_admin, sender=self)

    