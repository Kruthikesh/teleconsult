from apps.commons.constants import Specialisations
from apps.doctor.models import Specialisation

from django.db import migrations
import logging

logger = logging.getLogger(__name__)


def create_specialisations(apps, schema_editor):
    logger.info('Entering method - create_specialisations')

    """
        For MVP, we do not want to consider work items with request type any other than the ones that is mentioned in WorkItemRequestTypeConstants
    """

    specialisation_types = Specialisations.get_list_for_choices()
    for specialisation in specialisation_types:
        Specialisation.objects.get_or_create(name=specialisation)

    logger.info('Exiting method - create_specialisations')


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunPython(create_specialisations),
    ]
