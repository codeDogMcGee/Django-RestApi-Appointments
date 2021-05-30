from django.db import models

class Appointment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    appointment_start_time = models.DateTimeField(blank=False)
    appointment_end_time = models.DateTimeField(blank=False)
    customer_id = models.IntegerField(blank=False)
    employee_id = models.IntegerField(blank=False)

    def __str__(self):
        return f'Appointment: {self.appointment_start_time}\temployee={self.employee_id}\tcustomer={self.customer_id}'

    class Meta:
        ordering = ['appointment_start_time']

class PastAppointment(models.Model):
    created = models.DateTimeField(blank=False)
    appointment_start_time = models.DateTimeField(blank=False)
    appointment_end_time = models.DateTimeField(blank=False)
    customer_id = models.IntegerField(blank=False)
    employee_id = models.IntegerField(blank=False)

    def __str__(self):
        return f'PastAppointment: {self.appointment_start_time}\temployee={self.employee_id}\tcustomer={self.customer_id}'

    class Meta:
        ordering = ['appointment_start_time']