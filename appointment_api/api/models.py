from django.db import models
from django.utils import timezone

class Appointment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    customer_id = models.IntegerField(blank=False)
    employee_id = models.IntegerField(blank=False)

    def __str__(self):
        return f'StartTime={self.start_time} | EndTime={self.end_time} | Employee={self.employee_id} | Customer={self.customer_id}'

    class Meta:
        ordering = ['start_time']

class PastAppointment(models.Model):
    created = models.DateTimeField(blank=False)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    customer_id = models.IntegerField(blank=False)
    employee_id = models.IntegerField(blank=False)

    def __str__(self):
        return f'StartTime={self.start_time} | EndTime={self.end_time} | Employee={self.employee_id} | Customer={self.customer_id}'

    class Meta:
        ordering = ['start_time']

class HelperModel(models.Model):
    last_appointment_cleanup_time = models.DateTimeField(default=timezone.datetime(2000, 1, 1, 0, 0, 0))