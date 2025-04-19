from datetime import date
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import PartialUser, User
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

class RegisterStep1Serializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = PartialUser
        fields = ['full_name', 'email', 'phone_number']

    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Full name cannot be blank.")
        return value   

    def validate_email(self, value):
        try:
            django_validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email format.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already registered.")
        return value
    

class RegisterStep2Serializer(serializers.ModelSerializer):
    pan_card = serializers.CharField(required=True)
    aadhaar_card = serializers.CharField(required=True) 
    dob = serializers.DateField(required=True)
    
    class Meta:
        model = PartialUser
        fields = ['pan_card', 'aadhaar_card', 'dob']

    def validate_pan_card(self, value):
        pan_regex = RegexValidator(r'^[A-Z]{5}[0-9]{4}[A-Z]$', 'Invalid PAN card format.')
        pan_regex(value)
        if User.objects.filter(pan_card=value).exists():
            raise serializers.ValidationError("PAN card already registered.")
        return value

    def validate_aadhaar_card(self, value):
        if not value.isdigit() or len(value) != 12:
            raise serializers.ValidationError("Aadhaar card must be exactly 12 digits.")
        if User.objects.filter(aadhaar_card=value).exists():
            raise serializers.ValidationError("Aadhaar card already registered.")
        return value
    
    def validate_dob(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("User must be at least 18 years old.")
        return value
    
class RegisterStep3Serializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    password = serializers.CharField(write_only=True) 
    confirm_password = serializers.CharField(write_only=True)
    
    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials, please try again.")
        
        data['user'] = user
        return data

