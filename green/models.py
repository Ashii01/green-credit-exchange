from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager,  PermissionsMixin
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, full_name, phone_number, email, pan_card, aadhaar_card, dob, password=None, **extra_fields):
        if not full_name:
            raise ValueError('Full Name is required')
        if not phone_number:
            raise ValueError('Phone number is required')
        if not email:
            raise ValueError('Email is required')
        if not pan_card:
            raise ValueError('PAN card number is required')
        if not aadhaar_card:
            raise ValueError('Aadhar card number is required')
        if not dob:
            raise ValueError('Date of birth is required')

        user = self.model(
            full_name=full_name,
            phone_number=phone_number,
            email=self.normalize_email(email),
            pan_card=pan_card,
            aadhaar_card=aadhaar_card,
            dob=dob,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        if not username:
            raise ValueError('The username is required')
        if not email:
            raise ValueError('The email is required')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_admin=True,
            is_superuser=True,
            is_staff=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    username= models.CharField(max_length=25, unique=True, null=True, blank=True)
    full_name =models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    pan_card = models.CharField(max_length=10, unique=True)
    aadhaar_card = models.CharField(max_length=12, unique=True)
    dob = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] if is_superuser else ['full_name', 'phone_number', 'pan_card', 'aadhaar_card', 'dob']

    def __str__(self):
        return self.full_name


class PartialUser(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    pan_card = models.CharField(max_length=10, unique=True, null=True, blank=True)
    aadhaar_card = models.CharField(max_length=12, unique=True, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)  # hashed
    created_at = models.DateTimeField(auto_now_add=True)

