from django.core.exceptions import ValidationError
from api.utils.static_vars import MAX_SERVICES_PER_APPOINTMENT


def validate(appointment):
    services = appointment.services.split(',')
    if len(services) > MAX_SERVICES_PER_APPOINTMENT:
        raise ValidationError('Can not have more than %(max)s services per appointment.', params={'max': MAX_SERVICES_PER_APPOINTMENT})
    return appointment