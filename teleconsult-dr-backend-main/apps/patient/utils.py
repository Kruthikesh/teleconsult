from django.contrib.auth import authenticate
from rest_framework import serializers


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user


def create_user_account(email, password, insurance_number, aadhar_img, is_insurance_exists, first_name="",
                        last_name="", phone_number="", aadhar_no="", insurance_name=""):
    user = get_user_model().objects.create_user(
        email=email, password=password, first_name=first_name,
        last_name=last_name, phone_number=phone_number, aadhar_no=aadhar_no, aadhar_img=aadhar_img,
        is_insurance_exists=is_insurance_exists, insurance_name=insurance_name, insurance_number=insurance_number)
    return user


def convert_str_to_double(text):
    if not text:
        return None

    try:
        num = float(text)
        return num
    except:
        return None
