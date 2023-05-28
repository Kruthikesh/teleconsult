import os.path
import random

from django.db.models import QuerySet, Prefetch

from apps.commons.constants import TCDState
from apps.doctor.models import *
from apps.tcd.model_helpers import *
from apps.user.models import BaseClass
from main.settings.base import MEDIA_ROOT

from main.settings.settings import API_DOMAIN_URL


def generate_unique_id():
    # Generate a random 10-digit number
    while True:
        new_id = random.randint(1000000000, 9999999999)
        # Check if the number already exists in the database
        try:
            existing = TCD.objects.get(id=new_id)
        except TCD.DoesNotExist:
            # The number is unique, so return it
            return new_id


class TCDQueryManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        # This is to obtain data in the most optimal way by intimating ORM to leverage JOINS
        query_set = super().get_queryset()

        query_set = query_set.select_related("patient")
        query_set = query_set.select_related("doctor")
        query_set = query_set.select_related("specialisation")

        return query_set


class TCD(BaseClass):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name="tele_consultations", null=True)
    specialisation = models.ForeignKey(Specialisation, on_delete=models.SET_NULL, related_name="tele_consultations",
                                       null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, related_name="tele_consultations", null=True,
                               blank=True)
    is_active = models.BooleanField(default=True)
    state = models.CharField(max_length=512, null=True, blank=True, choices=TCDState.get_tuples_for_choices())
    objects = TCDQueryManager()  # type: ignore

    def save(self, *args, **kwargs):
        # Now create the folder within doctor folder with this id and upload all documents in there
        tcd_folder_dir = self.get_tcd_dir_path()
        is_path_exists = os.path.exists(tcd_folder_dir)
        if not is_path_exists:
            os.makedirs(tcd_folder_dir)

        super(TCD, self).save(*args, **kwargs)

    def to_dict(self):
        tcd_details = {
            'record_id': self.record_id,
            'created_at': self.created_at,
            'is_active': self.is_active,
            'state': self.state,
            'patient_details': self.patient.to_dict() if self.patient else {},
            'doctor_details': self.doctor.to_dict() if self.doctor else {},
            'specialisation': self.specialisation.name if self.specialisation else None,
            'patient_problems': [
                patient_problem.to_dict()
                for patient_problem in self.patient_problems.all().order_by('created_at')
            ]
        }

        if self.state == TCDState.CLOSED or not self.is_active:
            patient_review = PatientProblemReview.objects.filter(tcd=self).first()
            tcd_details['patient_review'] = patient_review.to_dict() if patient_review else {}

        return tcd_details

    def get_current_tcd_state(self):
        pass

    def get_tcd_dir_path(self):
        return os.path.join('tcd', str(self.record_id))

    class Meta(BaseClass.Meta):
        db_table = 'da_tcd'


class DoctorSuggestion(BaseClass):
    tcd = models.ForeignKey(TCD, on_delete=models.CASCADE, null=True, related_name="doctor_suggestions")
    ill_description = models.TextField(max_length=10280, null=True, blank=True)
    fee = models.CharField(max_length=512, null=True, blank=True)
    prescription_date = models.DateTimeField(default=datetime.now, blank=True)

    def to_dict(self):
        file_paths_for_examination_images = [
            API_DOMAIN_URL + 'media/' + doc_examination.image.name if doc_examination.image else None
            for doc_examination in self.doctor_examination_images.all()
        ]

        file_paths_for_prescription_images = [
            API_DOMAIN_URL + 'media/' + prescription_images.image.name if prescription_images.image else None
            for prescription_images in self.doctor_prescription_images.all()

        ]
        file_paths_for_video_interaction = [
            API_DOMAIN_URL + 'media/' + interaction_video.video.name if interaction_video.video else None
            for interaction_video in self.doctor_video_of_interaction.all()
        ]
        file_paths_for_video_suggestions = [
            API_DOMAIN_URL + 'media/' + suggestion_video.video.name if suggestion_video.video else None
            for suggestion_video in self.doctor_suggestions_videos.all()
        ]

        return {
            'record_id': self.record_id,
            'examination_images': [os.path.join(API_DOMAIN_URL, path) for path in file_paths_for_examination_images],
            'interaction_videos': [os.path.join(API_DOMAIN_URL, path) for path in file_paths_for_video_interaction],
            'ill_description': self.ill_description,
            'prescription_images': [os.path.join(API_DOMAIN_URL, path) for path in file_paths_for_prescription_images],
            'video_suggestions': [os.path.join(API_DOMAIN_URL, path) for path in file_paths_for_video_suggestions],
            'fee': self.fee,
            'prescription_date': self.prescription_date,
            'doctor_info': self.tcd.doctor.to_dict() if self.tcd.doctor else {}
        }

    class Meta(BaseClass.Meta):
        db_table = 'da_doctors_suggestion'


class PatientProblem(BaseClass):
    tcd = models.ForeignKey(TCD, on_delete=models.CASCADE, null=False, related_name="patient_problems")
    doctor_suggestion = models.OneToOneField(DoctorSuggestion, on_delete=models.CASCADE, null=True)
    problem_description = models.TextField(max_length=1024, null=False)
    physical_examination_before_tcd = models.TextField(max_length=1024, null=True, blank=True)
    medications_before_tcd = models.TextField(max_length=1024, null=True, blank=True)
    surgeries_before_tcd = models.TextField(max_length=1024, null=True, blank=True)
    treatment_response_before_tcd = models.TextField(max_length=1024, null=True, blank=True)
    current_expectations = models.TextField(max_length=1024, null=True, blank=True)

    def to_dict(self):
        file_paths_for_documents = [
            API_DOMAIN_URL + 'media/' + prob_details.document.name if prob_details.document else None
            for prob_details in self.patient_problem_tcd_documents.all()
        ]
        file_paths_for_videos = [
            API_DOMAIN_URL + 'media/' + prob_details.video.name if prob_details.video else None
            for prob_details in self.patient_problem_tcd_videos.all()
        ]
        file_paths_for_images = [
            API_DOMAIN_URL + 'media/' + prob_details.image.name if prob_details.image else None
            for prob_details in self.patient_problem_tcd_images.all()
        ]
        return {
            'record_id': self.record_id,
            'created_at': self.created_at,
            'problem_description': self.problem_description,
            'physical_examination_before_tcd': self.physical_examination_before_tcd,
            'medications_before_tcd': self.medications_before_tcd,
            'surgeries_before_tcd': self.surgeries_before_tcd,
            'treatment_response_before_tcd': self.treatment_response_before_tcd,
            'current_expectations': self.current_expectations,
            'patient_problem_tcd_images': file_paths_for_images,
            'patient_problem_tcd_documents': file_paths_for_documents,
            'patient_problem_tcd_videos': file_paths_for_videos,
            'doctor_suggestion': self.doctor_suggestion.to_dict() if self.doctor_suggestion else {},
            'doctor_info': self.tcd.doctor.to_dict() if self.tcd.doctor else {}
        }

    class Meta(BaseClass.Meta):
        db_table = 'da_patients_problem'


class PatientProblemsTCDVideos(BaseClass):
    patient_problems = models.ForeignKey(PatientProblem, on_delete=models.CASCADE,
                                         related_name="patient_problem_tcd_videos")
    video = models.FileField(upload_to=get_file_path_for_patient_tcd_videos, max_length=1023,
                             null=True, blank=True)

    class Meta(BaseClass.Meta):
        db_table = 'da_patients_problems_tcd_video'


class PatientProblemsTCDDocuments(BaseClass):
    patient_problems = models.ForeignKey(PatientProblem, on_delete=models.CASCADE,
                                         related_name="patient_problem_tcd_documents")
    document = models.FileField(upload_to=get_file_path_for_patient_tcd_documents, max_length=1023,
                                null=True, blank=True)

    class Meta(BaseClass.Meta):
        db_table = 'da_patients_problems_tcd_document'


class PatientProblemExplanationImages(BaseClass):
    patient_problems = models.ForeignKey(PatientProblem, on_delete=models.CASCADE,
                                         related_name="patient_problem_tcd_images")
    image = models.ImageField(upload_to=get_file_path_for_patient_tcd_documents)

    class Meta(BaseClass.Meta):
        db_table = 'da_patients_problems_tcd_images'


class DoctorExaminationImages(BaseClass):
    doctor_suggestion = models.ForeignKey(DoctorSuggestion, on_delete=models.CASCADE,
                                          related_name="doctor_examination_images")
    image = models.ImageField(upload_to=get_file_path_for_dr_examination_images)

    class Meta(BaseClass.Meta):
        db_table = 'da_doctors_examination_image'


class VideoOfInteraction(BaseClass):
    doctor_suggestion = models.ForeignKey(DoctorSuggestion, on_delete=models.CASCADE,
                                          related_name="doctor_video_of_interaction")
    video = models.FileField(upload_to=get_file_path_for_dr_interaction_video)

    class Meta(BaseClass.Meta):
        db_table = 'da_video_of_interaction'


class PrescriptionImage(BaseClass):
    doctor_suggestion = models.ForeignKey(DoctorSuggestion, on_delete=models.CASCADE,
                                          related_name="doctor_prescription_images")
    image = models.FileField(upload_to=get_file_path_for_dr_prescription)

    class Meta(BaseClass.Meta):
        db_table = 'da_doctors_prescription_image'


class VideoSuggestions(BaseClass):
    doctor_suggestion = models.ForeignKey(DoctorSuggestion, on_delete=models.CASCADE,
                                          related_name="doctor_suggestions_videos")
    video = models.FileField(upload_to=get_file_path_for_dr_video_suggestion)

    class Meta(BaseClass.Meta):
        db_table = 'da_doctors_video_suggestion'


class PatientProblemReview(BaseClass):
    tcd = models.OneToOneField(TCD, on_delete=models.CASCADE, null=False, related_name="patient_problem_reviews")
    feedback_description = models.TextField(max_length=10280, null=True, blank=True)
    feedback_rating = models.IntegerField(null=True, blank=True)

    def to_dict(self):
        file_paths_for_images = [
            API_DOMAIN_URL + 'media/' + review_image.image.name if review_image.image else None
            for review_image in self.review_images.all()
        ]
        file_paths_for_videos = [
            API_DOMAIN_URL + 'media/' + review_video.video.name if review_video.video else None
            for review_video in self.review_videos.all()
        ]

        return {
            'record_id': self.record_id,
            'created_at': self.created_at,
            'feedback_description': self.feedback_description,
            'review_images': file_paths_for_images,
            'review_videos': file_paths_for_videos,
            'feedback_rating': self.feedback_rating,
        }

    class Meta(BaseClass.Meta):
        db_table = 'da_patients_problem_review'


class PatientReviewImage(BaseClass):
    patient_review = models.ForeignKey(PatientProblemReview, on_delete=models.CASCADE, related_name="review_images")
    image = models.ImageField(upload_to=get_file_path_for_review_images)

    class Meta(BaseClass.Meta):
        db_table = 'da_patients_review_images'


class PatientReviewVideo(BaseClass):
    patient_review = models.ForeignKey(PatientProblemReview, on_delete=models.CASCADE, related_name="review_videos")
    video = models.FileField(upload_to=get_file_path_for_review_videos)

    class Meta(BaseClass.Meta):
        db_table = 'da_patients_review_video'
