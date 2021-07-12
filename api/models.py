from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import int_list_validator #MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

from api.managers import CustomUserManager
from api.utils.format_phone_number import format_phone_number
from api.validators import is_int, service_category_exists


class HelperSettingsModel(models.Model):
    last_appointment_cleanup_time = models.DateTimeField(default=timezone.datetime(2000, 1, 1, 0, 0, 0))


class GroupIdsModel(models.Model):
    group_id = models.IntegerField(null=True)
    group_name = models.CharField(max_length=100, blank=False, null=False)


class ApiUser(AbstractBaseUser, PermissionsMixin):
    # phone = models.CharField(_('phone number'), max_length=10, unique=True, blank=False, validators=[MinLengthValidator(10), is_int.validate])
    email = models.EmailField(_('email'), unique=True, max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, auto_created=True)    
    name = models.CharField(_('name'), max_length=100, blank=False)

    last_appointment_datetime = models.DateTimeField(null=True)
    last_appointment_other_user_id = models.IntegerField(null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class ServiceMenuModel(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    category = models.CharField(max_length=100, blank=False, null=False, validators=[service_category_exists.validate])
    price = models.FloatField(blank=False, null=False)
    time_minutes = models.IntegerField(blank=False, null=False)


class EmployeeScheduleModel(models.Model):
    '''
    One schedule record will be created for each employee
    '''
    
    employee = models.OneToOneField(ApiUser, on_delete=models.CASCADE, primary_key=True)

    days_off = models.CharField(max_length=1000, validators=[int_list_validator], blank=True, null=True) # list of comma seperated days [20210704, 20211124]

    monday_first_appointment = models.TimeField(blank=False, null=True)
    monday_last_appointment = models.TimeField(blank=False, null=True)

    tuesday_first_appointment = models.TimeField(blank=False, null=True)
    tuesday_last_appointment = models.TimeField(blank=False, null=True)

    wednesday_first_appointment = models.TimeField(blank=False, null=True)
    wednesday_last_appointment = models.TimeField(blank=False, null=True)

    thursday_first_appointment = models.TimeField(blank=False, null=True)
    thursday_last_appointment = models.TimeField(blank=False, null=True)

    friday_first_appointment = models.TimeField(blank=False, null=True)
    friday_last_appointment = models.TimeField(blank=False, null=True)

    saturday_first_appointment = models.TimeField(blank=False, null=True)
    saturday_last_appointment = models.TimeField(blank=False, null=True)

    sunday_first_appointment = models.TimeField(blank=False, null=True)
    sunday_last_appointment = models.TimeField(blank=False, null=True)

    


class Appointment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    customer = models.ForeignKey(ApiUser, related_name='customer', on_delete=models.CASCADE, blank=False, null=False)
    employee = models.ForeignKey(ApiUser, related_name='employee', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'StartTime={self.start_time} | EndTime={self.end_time} | Employee={self.employee} | Customer={self.customer}'

    class Meta:
        ordering = ['start_time']


class PastAppointment(models.Model):
    created = models.DateTimeField(blank=False, null=False)
    appointment_id = models.IntegerField(blank=False, null=False)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)
    customer = models.ForeignKey(ApiUser, related_name='past_appointment_customer', on_delete=models.CASCADE, blank=False, null=True)
    employee = models.ForeignKey(ApiUser, related_name='past_appointment_employee', on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return f'StartTime={self.start_time} | EndTime={self.end_time} | Employee={self.employee} | Customer={self.customer}'

    class Meta:
        ordering = ['start_time']


class EmailVerificationToken(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    key = models.CharField(max_length=200, unique=True) # can set default=some_key_gen_method to auto generate the key
    created = models.DateTimeField(auto_now_add=True)
    keep_alive_seconds = models.IntegerField(default=1800)


