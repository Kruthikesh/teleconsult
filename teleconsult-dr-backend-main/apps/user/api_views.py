import pyotp
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.commons.constants import UserTypes
from apps.commons.status_codes import UserStatusCodes, AppAuthStatusCodes, PatientStatusCodes, DoctorStatusCodes
from apps.doctor.models import *
from apps.patient.models import *
from apps.tcd.models import *
from main.settings import settings
from apps.patient.models import *
from apps.commons.utils import str2bool


def get_or_create_user_and_profile(email, name, user_type, password=None, phone_number=None, is_email_verified=True):
    user = BaseUser.objects.filter(email=email).first()
    if not user:
        user = BaseUser(email=email)
        user.set_password(password)
        user.is_email_verified = is_email_verified
        user.save()

    user_profile = None
    if user_type == UserTypes.PATIENT.value:
        user_profile, created = Patient.objects.get_or_create(user=user)

    # update the user name if not exists
    if name and not user_profile.name:
        user_profile.name = name
        user_profile.save()

    # update the phone number in case if it is not updated
    if phone_number and not user_profile.phone_number:
        user_profile.phone_number = phone_number
        user_profile.save()

    user_group, created = Group.objects.get_or_create(name=user_type)
    user_group.user_set.add(user)

    user.save()
    return user, user_profile


class SignUpAPI(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name', None)
        password = data.get('password', None)
        email = data.get('email', None)
        phone_number = data.get('phone_number', None)
        aadhar_card_number = data.get('aadhar_card_number', None)
        aadhar_img = data.get('aadhar_img', None)
        insurance_exists_str = data.get('insurance_exists', None)
        insurance_exists = str2bool(insurance_exists_str)
        if not name or not password or not email:
            return Response(UserStatusCodes.MISSING_FIELDS_FOR_REGISTRATION, status=status.HTTP_200_OK)

        # write logic here. For example
        existing_user = BaseUser.objects.filter(email=email).first()
        if existing_user:
            return Response(UserStatusCodes.SAME_USER_EXISTS, status=status.HTTP_200_OK)

        user_type = UserTypes.PATIENT.value

        user, user_profile = get_or_create_user_and_profile(email, name, user_type, password, phone_number, True)

        user_profile.aadhar_no = aadhar_card_number
        user_profile.aadhar_img = aadhar_img
        user_profile.is_insurance_exists = insurance_exists

        if insurance_exists:
            insurance_name = data.get('insurance_name', None)
            insurance_no = data.get('insurance_no', None)

            user_profile.insurance_name = insurance_name
            user_profile.insurance_number = insurance_no

        user_profile.save()

        response = UserStatusCodes.REGISTRATION_SUCCESS
        response['data'] = {
            'user': user_profile.to_dict()
        }
        return Response(response, status=status.HTTP_200_OK)


class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        if email is None or password is None:
            return Response(UserStatusCodes.LOGIN_FAILED, status=status.HTTP_200_OK)

        user = authenticate(email=email, password=password)
        print(user)
        
        if not user:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        if not user.is_active:
            return Response(UserStatusCodes.USER_NOT_ACTIVE, status=status.HTTP_200_OK)

        if not user.is_email_verified:
            return Response(UserStatusCodes.EMAIL_NOT_VERIFIED, status=status.HTTP_200_OK)

        if user.is_admin:
            return Response(UserStatusCodes.LOGIN_FAILED, status=status.HTTP_200_OK)

        token, created = Token.objects.get_or_create(user=user)
        
        user_type = user.groups.values_list('name').first()
        print(user_type)
        profile = None
        if UserTypes.DOCTOR.value in user_type:
            profile = Doctor.objects.filter(user=user).first()

        elif UserTypes.PATIENT.value in user_type:
            profile = Patient.objects.filter(user=user).first()


        response = AppAuthStatusCodes.USER_FOUND
        response['data'] = {
            'token': token.key,
            'profile': profile.to_dict() if profile else {},
        }

        request.session['Authorization'] = 'Token ' + token.key
        request.session['user_id'] = str(user.record_id)
        return Response(response, status=status.HTTP_200_OK)


class LogoutAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        header = request.session.get('Authorization', None)
        if header and header.startswith('Token '):
            del request.session['Authorization']
            token = header.split('Token ')[1]
            Token.objects.filter(key=token).delete()

        return Response(UserStatusCodes.USER_LOGGED_OUT, status=status.HTTP_200_OK)


class ProfileAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        loggedin_user = self.request.user

        user_profile = None
        user_groups = [grp for grp in loggedin_user.groups.values_list('name', flat=True)]
        if UserTypes.DOCTOR.value in user_groups:
            user_profile = loggedin_user.doctor
        elif UserTypes.PATIENT.value in user_groups:
            user_profile = loggedin_user.patient

        if not user_profile:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        response = UserStatusCodes.USER_DETAILS_OBTAINED
        response['data'] = user_profile.to_dict()
        return Response(response, status=status.HTTP_200_OK)
