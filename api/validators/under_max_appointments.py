
from django.core.exceptions import ValidationError
from api.models import Appointment
from api.utils.static_vars import MAX_APPOINTMENTS_PER_CUSTOMER


def validate(appointment):
    customer = appointment['customer']
    appointments = Appointment.objects.filter(customer=customer)

    if len(appointments) >= MAX_APPOINTMENTS_PER_CUSTOMER:
        raise ValidationError('Maximum appointments reached [%(max_appointments)s].', params={'max_appointments': MAX_APPOINTMENTS_PER_CUSTOMER})

    return appointment