import datetime
import os

from django.db import models

from apps.commons.constants import UserTypes
from apps.user.models import BaseClass, BaseUser
from main.settings.settings import MEDIA_ROOT, API_DOMAIN_URL
from django.core import validators
import uuid


def get_file_path_for_patient_aadhar(instance, filename):
    # Converting uploaded Image name to unique name using uuid
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    patient_folder_path = instance.get_patient_dir_path()

    patient_aadhar_folder_dir = os.path.join(patient_folder_path, 'aadhar')
    isExist = os.path.exists(patient_aadhar_folder_dir)
    if not isExist:
        os.makedirs(patient_aadhar_folder_dir)

    return os.path.join(patient_aadhar_folder_dir, filename)


class Patient(BaseClass):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='patient')
    patient_reg_id = models.CharField(max_length=256, default='000')
    name = models.CharField(max_length=256)
    phone_regex = validators.RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                            message="Phone number must be entered in the format: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    aadhar_no = models.CharField(max_length=12, unique=True, null=True)
    aadhar_img = models.ImageField(upload_to="aadhar/patient", max_length=1023,
                                   null=True, blank=True)

    is_insurance_exists = models.BooleanField(default=False)
    insurance_name = models.CharField(max_length=256, null=True)
    insurance_number = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        """
        Here we auto-generate the patient id.
        Ex: DD-MM-YYYY-0001, DD-MM-YYYY-0002 etc
        """
        todays_date = datetime.datetime.today().date()
        all_patients_registered_today = Patient.objects.filter(created_at__date=todays_date).count()

        date_str = todays_date.strftime("%m-%d-%Y")
        current_patient_count = str(all_patients_registered_today + 1)
        new_patient_id = date_str + current_patient_count
        self.patient_reg_id = new_patient_id

        # Now create the folder within patient folder with this id and upload all documents in there
        patient_folder_dir = os.path.join(MEDIA_ROOT, 'patient_files', new_patient_id)
        is_path_exists = os.path.exists(patient_folder_dir)
        if not is_path_exists:
            os.makedirs(patient_folder_dir)

        super(Patient, self).save(*args, **kwargs)

    def get_patient_dir_path(self):
        return os.path.join(MEDIA_ROOT, 'patient_files', self.patient_reg_id)

    def to_dict(self):
        return {
            'record_id': self.record_id,
            'patient_id': self.patient_reg_id,
            'user_type': UserTypes.PATIENT.value.lower(),
            'email': self.user.email,
            'name': self.name,
            'phone_number': self.phone_number,
            'aadhar_no': self.aadhar_no,
            'aadhar_img': (
                    API_DOMAIN_URL + 'media/' + self.aadhar_img.name) if self.aadhar_img else None,
            'is_insurance_exists': self.is_insurance_exists,
            'insurance_name': self.insurance_name if self.is_insurance_exists else None,
            'insurance_number': self.insurance_number if self.is_insurance_exists else None,
        }

    class Meta(BaseClass.Meta):
        db_table = 'da_patient'
