from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from datetime import timedelta


class Appointment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=50, blank=False)
    employee_name = models.CharField(max_length=50, blank=False)
    appointment_datetime = models.DateTimeField(blank=False, unique=True)
    owner = models.ForeignKey('auth.User', related_name='appointments', on_delete=models.CASCADE)

    @property
    def is_completed(self):
        """ If it's been an hour assume the appointment is completed. """
        return timezone.now() > self.appointment_datetime + timedelta(hours=1)

    def __str__(self):
        return f'Appointment at {self.appointment_datetime}\n\temployee={self.employee}\n\tcustomer={self.customer}'

    class Meta:
        ordering = ['appointment_datetime']


class Customer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone = models.IntegerField(blank=False, validators=[MinLengthValidator(10), MaxLengthValidator(10)])
    last_appointment_date = models.DateTimeField(blank=True, null=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} email={self.email} phone={self.phone} last_appointment={self.last_appointment_date}'

    class Meta:
        ordering = ['last_name']


class Employee(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone = models.IntegerField(blank=False, validators=[MinLengthValidator(10), MaxLengthValidator(10)])
    is_active = models.BooleanField(blank=False)
    is_manager = models.BooleanField(blank=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} manager={self.is_manager} active={self.is_active}'

    class Meta:
        ordering = ['last_name']