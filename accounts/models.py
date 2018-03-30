from django.db import models
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class GuestDetails(models.Model):
    email          = models.EmailField()
    mobile_number  = PhoneNumberField(default='9999999999')
    first_name     = models.CharField(max_length=255, default='John')
    last_name      = models.CharField(max_length=255, default='Miller')
    active         = models.BooleanField(default=True)
    updated        = models.DateTimeField(auto_now=True)
    timestamp      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class UserManager(BaseUserManager):
    def create_user(self, email, mobile_number, first_name, last_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an Email ID')
        if not password:
            raise ValueError('Users must have a Password')
        if not mobile_number:
            raise ValueError('Users must have a Mobile Number')
        if not first_name:
            raise ValueError('Users must have a First name')
        if not last_name:
            raise ValueError('Users must have a Last name')

        user_obj = self.model(
            email = self.normalize_email(email),
            mobile_number = mobile_number,
            first_name = first_name,
            last_name = last_name
        )
        user_obj.set_password(password)
        user_obj.staff  = is_staff
        user_obj.admin  = is_admin
        user_obj.active = is_active

        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, mobile_number, first_name, last_name, password=None):
        user = self.create_user(
            email,
            mobile_number,
            first_name,
            last_name,
            password = password,
            is_staff = True
        )
        return user

    def create_superuser(self, email, mobile_number, first_name, last_name, password=None):
        user = self.create_user(
            email,
            mobile_number,
            first_name,
            last_name,
            password = password,
            is_staff = True,
            is_admin = True
        )
        return user



class User(AbstractBaseUser):
    email          = models.EmailField(max_length=255, unique=True, default='abc123@gmail.com')
    mobile_number  = PhoneNumberField(unique=True)
    first_name     = models.CharField(max_length=255, default='John')
    last_name      = models.CharField(max_length=255, default='Miller')
    active         = models.BooleanField(default=True)
    staff          = models.BooleanField(default=False)
    admin          = models.BooleanField(default=False)
    timestamp      = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + self.last_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin
