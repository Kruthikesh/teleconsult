from apps.commons.constants import *


def configure_groups_and_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group

    # create groups
    Group.objects.get_or_create(name=UserTypes.DOCTOR.value)
    Group.objects.get_or_create(name=UserTypes.PATIENT.value)