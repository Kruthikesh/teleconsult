import os.path

from apps.patient.models import *
from datetime import datetime


def get_path_for_tcd_assets(instance, filename, prob_or_doc_suggestion, type_of_asset):
    # Converting uploaded Image name to unique name using uuid
    ext = filename.split('.')[-1]
    filename = "%s-%s.%s" % (uuid.uuid4(), datetime.now().strftime("%d-%m-%Y"), ext)

    tcd_folder_path = None
    if prob_or_doc_suggestion == 'problem_details':
        tcd_folder_path = instance.patient_problems.tcd.get_tcd_dir_path()
    elif prob_or_doc_suggestion == 'patient_reviews':
        tcd_folder_path = instance.patient_review.tcd.get_tcd_dir_path()
    elif prob_or_doc_suggestion == 'doctor_suggestion':
        tcd_folder_path = instance.doctor_suggestion.tcd.get_tcd_dir_path()

    if not tcd_folder_path:
        return None

    patient_tcd_videos_folder_dir = os.path.join(tcd_folder_path, prob_or_doc_suggestion, type_of_asset)
    is_path_exists = os.path.exists(patient_tcd_videos_folder_dir)
    if not is_path_exists:
        os.makedirs(patient_tcd_videos_folder_dir, exist_ok=True)

    return os.path.join(patient_tcd_videos_folder_dir, filename)


def get_file_path_for_patient_tcd_videos(instance, filename):
    return get_path_for_tcd_assets(instance, filename, 'problem_details', 'tcd_videos')


def get_file_path_for_patient_tcd_documents(instance, filename):
    return get_path_for_tcd_assets(instance, filename, 'problem_details', 'tcd_documents')


def get_file_path_for_patient_tcd_images(instance, filename):
    return get_path_for_tcd_assets(instance, filename, 'problem_details', 'tcd_images')


def get_file_path_for_dr_examination_images(instance, filename):
    return get_path_for_tcd_assets(instance, filename, 'doctor_suggestion', 'examination_images')


def get_file_path_for_dr_interaction_video(instance, filename):
    return get_path_for_tcd_assets(instance, filename, 'doctor_suggestion', 'interaction_videos')


def get_file_path_for_dr_prescription(instance, filename):
    return get_path_for_tcd_assets(instance, filename, 'doctor_suggestion', 'prescription_images')


def get_file_path_for_dr_video_suggestion(instance, filename):
    return get_path_for_tcd_assets(instance, filename, 'doctor_suggestion', 'video_suggestions')


def get_file_path_for_review_images(instance, filename):
    return get_path_for_tcd_assets(instance, filename, 'patient_reviews', 'review_images')


def get_file_path_for_review_videos(instance, filename):
    return get_path_for_tcd_assets(instance, filename, 'patient_reviews', 'review_videos')
