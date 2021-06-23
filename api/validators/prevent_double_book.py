from django.core.exceptions import ValidationError
import pytz
from django.conf import settings
from ..models import Appointment


def validate(appointment):

    server_timezone = pytz.timezone(settings.TIME_ZONE)

    appointment_start_datetime_tz = appointment['start_time'].astimezone(server_timezone)
    appointment_end_datetime_tz = appointment['end_time'].astimezone(server_timezone)

    appointment_start_time_tz = appointment_start_datetime_tz.time()
    appointment_end_time_tz = appointment_end_datetime_tz.time()

    appointment_date_utc = appointment['start_time'].astimezone(pytz.utc).date() # convert to UTC to compare with server
    appointments_for_date = Appointment.objects.filter(start_time__date=appointment_date_utc)

    for existing_appointment in appointments_for_date:

        # convert existing appointment times from default utc to server timezone
        existing_appointment.start_time = existing_appointment.start_time.astimezone(server_timezone).time()
        existing_appointment.end_time = existing_appointment.end_time.astimezone(server_timezone).time()

        employee_is_same = appointment['employee'] == existing_appointment.employee
        customer_is_same = appointment['customer'] == existing_appointment.customer

        # check for overlap at the front, and either the customer or employee matches
        error = False
        if (employee_is_same or customer_is_same) and appointment_start_time_tz < existing_appointment.start_time and appointment_end_time_tz > existing_appointment.start_time:
            error = True
        
        # check for overlap at the end
        elif (employee_is_same or customer_is_same) and  appointment_start_time_tz < existing_appointment.end_time and appointment_end_time_tz > existing_appointment.end_time:
            error = True

        # check if inside of other existing appointment
        elif (employee_is_same or customer_is_same) and  appointment_start_time_tz >= existing_appointment.start_time and appointment_end_time_tz <= existing_appointment.end_time:
            error = True


        if error:
            appointment_string = f'[ {appointment_start_time_tz} - {appointment_end_time_tz} ]'
            existing_appointment_string = f'[ {existing_appointment.start_time} - {existing_appointment.end_time} ]'
            raise ValidationError( 'Appointment %(appointment)s overlapps with the existing appointment %(existing_appointment)s', 
                                  params={'appointment': appointment_string, 'existing_appointment': existing_appointment_string})

    return appointment
