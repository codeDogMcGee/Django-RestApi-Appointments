from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from datetime import timedelta
from api.validators import validate_is_int


class Customer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone = models.CharField(max_length=10, blank=False, validators=[MinLengthValidator(10), validate_is_int])
    owner = models.ForeignKey('auth.User', related_name='customers', on_delete=models.CASCADE)

    last_appointment_date = models.DateTimeField(blank=False, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_appointment_date']


class Employee(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone = models.CharField(max_length=10, blank=False, validators=[MinLengthValidator(10), validate_is_int])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name']


class Appointment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    appointment_datetime = models.DateTimeField(blank=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='appointments', on_delete=models.CASCADE)

    @property
    def is_completed(self):
        """ If it's been an hour assume the appointment is completed. """
        return timezone.now() > self.appointment_datetime + timedelta(hours=1)

    def __str__(self):
        return f'Appointment at {self.appointment_datetime}\n\temployee={self.employee}\n\tcustomer={self.customer}'

    class Meta:
        ordering = ['appointment_datetime']
