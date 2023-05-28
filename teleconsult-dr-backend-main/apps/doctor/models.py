import os
import uuid

from django.db import models

from apps.commons.constants import UserTypes
from apps.user.models import BaseClass, BaseUser
from django.core import validators
from main.settings.settings import MEDIA_ROOT


def get_file_path_for_doctor_aadhar(instance, filename):
    # Converting uploaded Image name to unique name using uuid
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    doctor_folder_path = instance.get_doctor_dir_path()

    doctor_aadhar_folder_dir = os.path.join(doctor_folder_path, 'aadhar')
    return os.path.join(doctor_aadhar_folder_dir, filename)


class Specialisation(BaseClass):
    name = models.CharField(max_length=512, null=True, blank=True)


class Doctor(BaseClass):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='doctor')
    doctor_id = models.CharField(max_length=256, null=False, blank=False)
    name = models.CharField(max_length=512, null=True, blank=True)
    phone_regex = validators.RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                            message="Phone number must be entered in the format: '+999999999'.")  # NOTSURE
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    specialisation = models.ForeignKey(Specialisation, on_delete=models.SET_NULL, related_name='specialisation', null=True)

    def save(self, *args, **kwargs):
        """
        Here we auto-generate the doctor id.
        Ex: doc-0001, doc-0002 etc
        """
        all_doctors = Doctor.objects.all().count()

        new_doctor_count = str(all_doctors + 1)
        new_doctor_id = 'doc-' + new_doctor_count
        self.doctor_id = new_doctor_id

        # Now create the folder within doctor folder with this id and upload all documents in there
        doctor_folder_dir = self.get_doctor_dir_path()
        is_path_exists = os.path.exists(doctor_folder_dir)
        if not is_path_exists:
            os.makedirs(doctor_folder_dir)

        super(Doctor, self).save(*args, **kwargs)

    def get_doctor_dir_path(self):
        return os.path.join('doctor_files', self.doctor_id)

    def to_dict(self):
        return {
            'record_id': self.record_id,
            'doctor_id': self.doctor_id,
            'user_type': UserTypes.DOCTOR.value.lower(),
            'email': self.user.email,
            'is_password_set': True if self.user.password else False,
            'name': self.name,
            'phone_number': self.phone_number,
            'specialisation': self.specialisation.name if self.specialisation else None,
        }

    def __str__(self):
        return self.name

    class Meta(BaseClass.Meta):
        db_table = 'da_doctor'
