from django.db import models


class Appointment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=50, blank=False)
    employee_name = models.CharField(max_length=50, blank=False)
    appointment_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['appointment_datetime']