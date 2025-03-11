from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(error_messages={"invalid": "Invalid email format."})
    phone_number = serializers.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must be exactly 10 digits.')],
    )
    aadhaar_card = serializers.CharField(
        max_length=12,
        validators=[RegexValidator(r'^\d{12}$', 'Aadhaar must be exactly 12 digits.')],
    )
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],  # Django's built-in password validation
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'pan_card', 'aadhaar_card', 'dob', 'password', 'confirm_password']

    def validate(self, data):
        """Ensure password and confirm_password match."""
        password = data.get("password")  # ✅ Now safe to use `.get()`
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        return data

    def create(self, validated_data):
        """Remove confirm_password before saving the user."""
        validated_data.pop('confirm_password')  # ✅ Remove confirm_password before saving
        user = User.objects.create_user(**validated_data)
        return user
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials, please try again.")
        
        data['user'] = user
        return data

