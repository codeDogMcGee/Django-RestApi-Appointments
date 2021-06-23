from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

from api.managers import CustomUserManager
from api.utils.format_phone_number import format_phone_number
from api.validators import is_int


class HelperSettingsModel(models.Model):
    last_appointment_cleanup_time = models.DateTimeField(default=timezone.datetime(2000, 1, 1, 0, 0, 0))


class GroupIdsModel(models.Model):
    group_id = models.IntegerField(null=True)
    group_name = models.CharField(max_length=100, blank=False, null=False)


class ApiUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(_('phone number'), max_length=10, unique=True, blank=False, validators=[MinLengthValidator(10), is_int.validate])
    created = models.DateTimeField(auto_now_add=True, auto_created=True)    
    name = models.CharField(_('name'), max_length=100, blank=False)

    last_appointment_datetime = models.DateTimeField(null=True)
    last_appointment_other_user_id = models.IntegerField(null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name} | {format_phone_number(self.phone)}'


class Appointment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    # customer_id = models.IntegerField(blank=False)
    # employee_id = models.IntegerField(blank=False)
    customer = models.ForeignKey(ApiUser, related_name='customer', on_delete=models.CASCADE, blank=False, null=True)
    employee = models.ForeignKey(ApiUser, related_name='employee', on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return f'StartTime={self.start_time} | EndTime={self.end_time} | Employee={self.employee} | Customer={self.customer}'

    class Meta:
        ordering = ['start_time']


class PastAppointment(models.Model):
    created = models.DateTimeField(blank=False, null=False)
    appointment_id = models.IntegerField(blank=False, null=False)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)
    # customer_id = models.IntegerField(blank=False, null=False)
    # employee_id = models.IntegerField(blank=False, null=False)
    customer = models.ForeignKey(ApiUser, related_name='past_appointment_customer', on_delete=models.CASCADE, blank=False, null=True)
    employee = models.ForeignKey(ApiUser, related_name='past_appointment_employee', on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return f'StartTime={self.start_time} | EndTime={self.end_time} | Employee={self.employee} | Customer={self.customer}'

    class Meta:
        ordering = ['start_time']