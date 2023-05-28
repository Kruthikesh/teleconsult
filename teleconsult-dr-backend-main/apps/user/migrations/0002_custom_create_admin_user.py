from django.db import migrations
import logging

logger = logging.getLogger(__name__)


def create_admin(apps, schema_editor):
    from apps.user.models import BaseUser

    try:
        logger.info("Checking if admin user details exists")
        user = BaseUser.objects.filter(email="admin@tcd.com", is_superuser=True)
        if user:
            logger.info("Admin user already exists")
            return

        BaseUser.objects.create_user(
            email="admin@tcd.com",
            password="admin",
            is_active=True,
            is_superuser=True,
            is_staff=False,
        )

        logger.info("Ådmin user created")
        return
    except Exception as e:
        logger.info(str(e))
        logger.info("Exception occurred while checking/creating the admin")
        return


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
