# from rest_framework import serializers
# from django.contrib.auth.models import User
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password
# from .models import Patient
# User Serializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Patient
User = get_user_model()
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)
class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff','aadhar_no','aadhar_img','email','password')
         read_only_fields = ('id', 'is_active', 'is_staff')
    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)
    name=serializers.CharField(write_only=True, required=True)
    phone_number=serializers.CharField(write_only=True, required=True)
    aadhar_no=serializers.CharField(write_only=True, required=True)
    is_insurance_exists=serializers.CharField(write_only=True, required=True)
    insurance_name=serializers.CharField(write_only=True, required=True)
    class Meta:
        model=Patient
        fields = ( "name", "phone_number", "aadhar_no","is_insurance_exists","insurance_name","aadhar_img")
    def create(self, validated_data):
      user = Patient.objects.create(
      email=validated_data['email'],
      password=validated_data['password'],
      name=validated_data['name'],
      phone=validated_data['phone'],
      aadhar_no=validated_data['aadhar_no'],
      aadhar_img=validated_data['aadhar_img'],
      is_insurance_exists=validated_data['is_insurance_exists'],
      insurance_name=validated_data['insurance_name']
    )
      user.save()
      return user
class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = Patient
        fields = ('email','password','aadhar_no','phone_number','aadhar_img','is_insurance_exists','insurance_name','insurance_number')

    def validate_email(self, value):
        user = Patient.objects.filter(email=email)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value
    # class Meta:
    #     model = Patient
    #     fields = ('id', 'username', 'email', 'password','phone_number','aadhar_no','is_insurance_exists','insurance_name')
    #     extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = Patient.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

    #     return user
