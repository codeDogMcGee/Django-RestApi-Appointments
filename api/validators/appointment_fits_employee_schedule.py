from datetime import datetime
from django.core.exceptions import ValidationError
import pytz
from django.conf import settings
from api.models import EmployeeScheduleModel


SERVER_TIMEZONE = pytz.timezone(settings.TIME_ZONE)


def _localize_date_string(date_string):
    if date_string:
        return SERVER_TIMEZONE.localize(datetime.strptime(date_string, '%Y%m%d')).date()
    else:
        return None


def validate(appointment):
    timezone_to_use = SERVER_TIMEZONE # pytz.utc 

    appointment_start_datetime = appointment['start_time'].astimezone(timezone_to_use)
    appointment_start_time = appointment_start_datetime.time()
    appointment_weekday = appointment_start_datetime.weekday()
    appointment_date = appointment_start_datetime.date()

    error = False
    employee_schedule = EmployeeScheduleModel.objects.get(pk=appointment['employee'])
    if employee_schedule:

        # convert days_off from comma seperated string to list of dates
        days_off = employee_schedule.days_off.split(',')
        days_off = [_localize_date_string(day_off) for day_off in days_off]

        schedule_weekdays = {
            0: (employee_schedule.monday_first_appointment, employee_schedule.monday_last_appointment),
            1: (employee_schedule.tuesday_first_appointment, employee_schedule.tuesday_last_appointment),
            2: (employee_schedule.wednesday_first_appointment, employee_schedule.wednesday_last_appointment),
            3: (employee_schedule.thursday_first_appointment, employee_schedule.thursday_last_appointment),
            4: (employee_schedule.friday_first_appointment, employee_schedule.friday_last_appointment),
            5: (employee_schedule.saturday_first_appointment, employee_schedule.saturday_last_appointment),
            6: (employee_schedule.sunday_first_appointment, employee_schedule.sunday_last_appointment),
        }

        min_start_time_local_tz, max_start_time_local_tz = schedule_weekdays[appointment_weekday]

        if min_start_time_local_tz and max_start_time_local_tz:

            if appointment_start_time < min_start_time_local_tz or appointment_start_time > max_start_time_local_tz:
                error = True

            if appointment_date in days_off:
                error = True

        else:  # employee has a null value for this day/time
            error = True
        
    else:  # no schedule has been created for this employee
        error = True

    if error:
        raise ValidationError( 'Appointment is outside of employee schedule time.')

    return appointment
