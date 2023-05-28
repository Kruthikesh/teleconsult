import traceback

from django.db import transaction
from django.http import *

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.commons.constants import Specialisations
from apps.commons.status_codes import *
from apps.patient.utils import convert_str_to_double
from apps.tcd.models import *
from apps.patient.models import *
from django.utils.timezone import now

import datetime


class TCDFeedbackAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        data = request.data

        tcd_id = self.kwargs.get('tcd_id', None)
        tcd = TCD.objects.filter(record_id=tcd_id).first()
        if not tcd:
            return Response(TCDStatusCodes.TCD_NOT_FOUND, status=status.HTTP_200_OK)

        feedback_description = data.get('feedback_description', None)
        feedback_rating = data.get('feedback_rating', None)
        if not feedback_description and not feedback_rating:
            return Response(TCDStatusCodes.MISSING_FIELDS_FOR_FEEDBACK, status=status.HTTP_200_OK)

        try:
            with transaction.atomic():
                if feedback_rating:
                    feedback_rating = convert_str_to_double(feedback_rating)

                patient_review = PatientProblemReview.objects.create(tcd=tcd,
                                                                     feedback_description=feedback_description,
                                                                     feedback_rating=feedback_rating)

                tcd.is_active = False
                tcd.state = TCDState.CLOSED
                tcd.save()

                feedback_video_input = data.get('feedback_video', None)
                
                if feedback_video_input:
                    feedback_video = request.FILES.get('feedback_video', None)
                    if feedback_video:
                        PatientReviewVideo.objects.create(patient_review=patient_review,
                                                      video=feedback_video)
                
                feedback_images = request.FILES.getlist('feedback_images', None)
                if feedback_images:
                    for image_code in feedback_images:
                        PatientReviewImage.objects.create(patient_review=patient_review, image=image_code)

                return Response(TCDStatusCodes.TCD_FEEDBACK_UPDATED, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            print(traceback.print_exc())
            return HttpResponseServerError()

    def get(self, request, **kwargs):
        feedback_id = self.kwargs.get('feedback_id', None)
        review = PatientProblemReview.objects.filter(record_id=feedback_id).first()
        if not review:
            return Response(TCDStatusCodes.TCD_FEEDBACK_NOT_FOUND, status=status.HTTP_200_OK)

        response = TCDStatusCodes.TCD_FEEDBACK_OBTAINED
        response['data'] = review.to_dict()
        return Response(response, status=status.HTTP_200_OK)


class TCDAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, **kwargs):
        data = request.data

        tcd_id = self.kwargs.get('tcd_id', None)
        tcd = TCD.objects.filter(record_id=tcd_id).first()
        if not tcd:
            return Response(TCDStatusCodes.TCD_NOT_FOUND, status=status.HTTP_200_OK)

        try:
            with transaction.atomic():
                tcd.is_active = False
                tcd.state = TCDState.CLOSED
                tcd.save()

        except Exception as e:
            print(str(e))
            print(traceback.print_exc())
            return HttpResponseServerError()

    def get(self, request, **kwargs):
        loggedin_user = self.request.user

        user_profile = None
        user_groups = [grp for grp in loggedin_user.groups.values_list('name', flat=True)]
        if UserTypes.DOCTOR.value in user_groups:
            user_profile = loggedin_user.doctor
        elif UserTypes.PATIENT.value in user_groups:
            user_profile = loggedin_user.patient

        tcd_id = self.kwargs.get('tcd_id', None)
        tcd = TCD.objects.filter(record_id=tcd_id).first()

        if not user_profile and not tcd:
            return Response(TCDStatusCodes.MISSING_PATIENT_OR_TCD_DETAILS, status=status.HTTP_200_OK)

        if tcd:
            # this condition will be problem_explanation and not patient
            response = TCDStatusCodes.TCD_FOUND
            response['data'] = tcd.to_dict()
            return Response(response, status=status.HTTP_200_OK)

        all_tcd_details = []
        if UserTypes.DOCTOR.value in user_groups:
            all_tcd_details = [
                tcd.to_dict()
                for tcd in TCD.objects.filter(doctor=user_profile)
            ]
        elif UserTypes.PATIENT.value in user_groups:
            all_tcd_details = [
                tcd.to_dict()
                for tcd in TCD.objects.filter(patient=user_profile)
            ]

        response = PatientProblemStatusCodes.PROBLEM_EXPLANATION_FOUND
        response['data'] = all_tcd_details
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        data = request.data
        loggedin_user = self.request.user
        patient = loggedin_user.patient

        if not patient:
            return Response(PatientStatusCodes.PATIENT_NOT_FOUND, status=status.HTTP_200_OK)

        tcd_id = self.kwargs.get('tcd_id', None)
        tcd = TCD.objects.filter(record_id=tcd_id).first()
        if tcd_id and not tcd:
            return Response(TCDStatusCodes.TCD_NOT_FOUND, status=status.HTTP_200_OK)

        problem_description = data.get('problem_description', None)
        current_expectations = data.get('current_expectations', None)
        if not tcd:
            # Mandatory for a new consultation
            if not problem_description or not current_expectations:
                return Response(PatientProblemStatusCodes.MISSING_FIELDS_FOR_PROBLEM_EXPLANATION,
                                status=status.HTTP_200_OK)

        physical_examination_before_tcd = data.get('physical_examination_before_tcd', None)
        medications_before_tcd = data.get('medications_before_tcd', None)
        surgeries_before_tcd = data.get('surgeries_before_tcd', None)
        treatment_response_before_tcd = data.get('treatment_response_before_tcd', None)
        try:
            with transaction.atomic():
                specialisation_obj, _ = Specialisation.objects.get_or_create(name=Specialisations.ORTHOPAEDIC)
                if not tcd:
                    tcd = TCD.objects.create(patient=patient, specialisation=specialisation_obj,
                                             is_active=True, state=TCDState.OPEN)

                patient_problem = PatientProblem.objects.create(
                    tcd=tcd,
                    problem_description=problem_description,
                    physical_examination_before_tcd=physical_examination_before_tcd,
                    medications_before_tcd=medications_before_tcd,
                    surgeries_before_tcd=surgeries_before_tcd,
                    treatment_response_before_tcd=treatment_response_before_tcd,
                    current_expectations=current_expectations
                )

                tcd.state = TCDState.PATIENT_INPUT_SUBMITTED
                tcd.save()

                problem_explanation_video = request.FILES.get('problem_explanation_video', None)
                PatientProblemsTCDVideos.objects.create(patient_problems=patient_problem,
                                                        video=problem_explanation_video)

                problem_explanation_images = request.FILES.getlist('problem_explanation_images', None)
                for image in problem_explanation_images:
                    PatientProblemExplanationImages.objects.create(patient_problems=patient_problem,
                                                                   image=image)

                response = PatientStatusCodes.PATIENT_PROBLEM_UPLOADED
                response['data'] = {
                    'patient': patient_problem.to_dict(),
                }
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            print(traceback.print_exc())
            return HttpResponseServerError()


class DoctorResponseAPI(APIView):
    def post(self, request, **kwargs):
        data = request.data

        problem_id = self.kwargs.get('problem_id', None)
        patient_problem = PatientProblem.objects.filter(record_id=problem_id).first()
        if not patient_problem:
            return Response(PatientProblemStatusCodes.PROBLEM_EXPLANATION_NOT_FOUND, status=status.HTTP_200_OK)

        tcd = patient_problem.tcd
        fee = data.get('fee', None)
        ill_description = data.get('ill_description', None)

        if not fee or not ill_description:
            return Response(DoctorStatusCodes.NO_DOCTOR_RESPONSE, status=status.HTTP_200_OK)

        try:
            with transaction.atomic():
                doctor = patient_problem.tcd.doctor
                if not doctor:
                    return Response(DoctorStatusCodes.DOCTOR_NOT_FOUND, status=status.HTTP_200_OK)

                doctor_suggestion = DoctorSuggestion.objects.create(
                    tcd=tcd,
                    fee=fee,
                    ill_description=ill_description,
                    prescription_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

                patient_problem.doctor_suggestion = doctor_suggestion
                patient_problem.tcd.state = TCDState.DOCTOR_SUGGESTION_SUBMITTED
                patient_problem.tcd.save()

                patient_problem.tcd.doctor = doctor
                patient_problem.tcd.save()

                interaction_video = request.FILES.get('interaction_video', None)
                if interaction_video:
                    VideoOfInteraction.objects.create(doctor_suggestion=doctor_suggestion, video=interaction_video)

                suggestion_video = request.FILES.get('suggestion_video', None)
                if suggestion_video:
                    VideoSuggestions.objects.create(doctor_suggestion=doctor_suggestion, video=suggestion_video)

                examination_images = request.FILES.getlist('examination_images', None)
                for image in examination_images:
                    DoctorExaminationImages.objects.create(doctor_suggestion=doctor_suggestion, image=image)

                prescription_images = request.FILES.getlist('prescription_images', None)
                for image in prescription_images:
                    DoctorExaminationImages.objects.create(doctor_suggestion=doctor_suggestion, image=image)

                response = DoctorStatusCodes.DOCTOR_RESPONSE_UPLOADED
                response['data'] = {
                    'Doctor_Response': doctor_suggestion.to_dict()
                }
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            print(traceback.print_exc())
            return HttpResponseServerError()

    def get(self, request, **kwargs):
        suggestion_id = self.kwargs.get('doctor_response_id', None)
        try:
            doctor_suggestion = DoctorSuggestion.objects.filter(record_id=suggestion_id).first()
            if not doctor_suggestion:
                return Response(DoctorStatusCodes.NO_DOCTOR_RESPONSE, status=status.HTTP_200_OK)

            response = DoctorStatusCodes.DOCTOR_RESPONSE_FOUND
            response['data'] = doctor_suggestion.to_dict()
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(DoctorStatusCodes.DOCTOR_RESPONSE_FETCH_FAILED, status=status.HTTP_200_OK)


class PatientProblemExplainationAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, **kwargs):
        # use this method for update
        return Response({}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def get(self, request, **kwargs):
        problem_explanation_id = self.kwargs.get('problem_explanation_id', None)
        problem_explanation = PatientProblem.objects.filter(record_id=problem_explanation_id).first()

        if not problem_explanation_id:
            return Response(PatientProblemStatusCodes.PROBLEM_EXPLANATION_NOT_FOUND, status=status.HTTP_200_OK)

        response = PatientProblemStatusCodes.PROBLEM_EXPLANATION_FOUND
        response['data'] = problem_explanation.to_dict()
        return Response(response, status=status.HTTP_200_OK)


class UserRatingsAndReviewsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        loggedin_user = self.request.user

        user_groups = [grp for grp in loggedin_user.groups.values_list('name', flat=True)]
        if UserTypes.DOCTOR.value in user_groups:
            doctor = loggedin_user.doctor
            tcds = TCD.objects.filter(doctor=doctor).all()
            if not tcds:
                return Response(TCDStatusCodes.TCD_NOT_FOUND, status=status.HTTP_200_OK)
            response = TCDStatusCodes.TCD_FEEDBACK_OBTAINED
            for tcd in tcds:
                problem_review_by_patient = PatientProblemReview.objects.filter(tcd = tcd).first()
                if problem_review_by_patient:
                    response['data'] = problem_review_by_patient.to_dict()
            if not response['data']:
                return Response(PatientProblemStatusCodes.REVIEWS_BY_PATIENT_NOT_FOUND, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_200_OK)


        elif UserTypes.PATIENT.value in user_groups:
            patient = loggedin_user.patient
            tcds_of_patient = TCD.objects.filter(patient = patient).all()

            if not tcds_of_patient:
                return Response(TCDStatusCodes.TCD_NOT_FOUND, status=status.HTTP_200_OK)
            response = TCDStatusCodes.TCD_FEEDBACK_OBTAINED
            for tcd_of_patient in tcds_of_patient:
                problem_review_by_patient = PatientProblemReview.objects.filter(tcd = tcd_of_patient).first()

                if problem_review_by_patient:
                    response['data'] = problem_review_by_patient.to_dict()
                
            if not response['data']:
                return Response(PatientProblemStatusCodes.REVIEWS_BY_PATIENT_NOT_FOUND, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_200_OK)

        else:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)
