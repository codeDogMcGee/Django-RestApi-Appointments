from django.db import models
from django.utils import timezone
from datetime import timedelta
# from django.core.validators import MinLengthValidator
# from api.validators import validate_is_int


class Customer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=False)
    # last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    # phone = models.CharField(max_length=10, blank=False, validators=[MinLengthValidator(10), validate_is_int])
    # last_appointment_date = models.DateTimeField(blank=False, null=True)

    def __str__(self):
        return f'{self.first_name}'

    class Meta:
        ordering = ['email']


class Employee(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=False)
    # last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    # phone = models.CharField(max_length=10, blank=False, validators=[MinLengthValidator(10), validate_is_int])
    # last_appointment_date = models.DateTimeField(blank=False, null=True)
    # is_active = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return f'{self.first_name}'

    class Meta:
        ordering = ['email']


class Appointment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    appointment_datetime = models.DateTimeField(blank=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    @property
    def is_completed(self):
        """ If it's been an hour assume the appointment is completed. """
        return timezone.now() > self.appointment_datetime + timedelta(hours=1)

    def __str__(self):
        return f'Appointment at {self.appointment_datetime}\n\temployee={self.employee}\n\tcustomer={self.customer}'

    class Meta:
        ordering = ['appointment_datetime']
