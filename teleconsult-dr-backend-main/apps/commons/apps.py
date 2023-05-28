from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CommonsConfig(AppConfig):
    name = 'apps.commons'

    def ready(self):
        from apps.commons.signals import configure_groups_and_permissions
        post_migrate.connect(configure_groups_and_permissions, sender=self)