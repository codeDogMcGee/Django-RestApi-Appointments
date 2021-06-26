from asgiref.sync import sync_to_async
from django.utils import timezone

from api.models import Appointment, PastAppointment, HelperSettingsModel
from api.serializers import HelperSettingsSerializer, PastAppointmentSerializer
from api.utils.static_vars import DELETE_OLD_APPOINTEMENTS_EVERY_N_DAYS, MAX_APPOINTMENT_AGE_DAYS


def _move_completed_appointments_to_past_appointments():
    appointments = Appointment.objects.all()
    for appointment in appointments:
        if timezone.now() > appointment.end_time:

            past_appointment_object = {
                'appointment_id': appointment.id,
                'start_time' : appointment.start_time, 
                'end_time' : appointment.end_time, 
                'customer' : appointment.customer_id,
                'employee' : appointment.employee_id,
                'created' : appointment.created
            }

            print('\n\nPAST APPT:\n', past_appointment_object, '\n\n')

            past_appointment_serializer = PastAppointmentSerializer(data=past_appointment_object)
            
            # save any appointment that is completed to PastAppointments and delete from Appointments
            if past_appointment_serializer.is_valid():
                print('\n\nAPPT TO DELETE:\n', appointment, '\n\n')
                past_appointment_serializer.save()
                appointment.delete()
            else:
                print(f'\nERROR SERIALIZING DATA: {past_appointment_serializer.errors}\n')


def _instatiate_helper_model():
    helper_object = {
        'last_appointment_cleanup_time': timezone.now() - timezone.timedelta(days=30)
    }
    helpers_serializer = HelperSettingsSerializer(data=helper_object)

    if helpers_serializer.is_valid():
        helpers_serializer.save()
    else:
        raise Exception(f'\nERROR INSTATIATING HELPER MODEL: {helpers_serializer.errors}\n')


def _create_helper_object_if_not_exits():
    helpers = HelperSettingsModel.objects.all()

    if len(helpers) == 0:
        _instatiate_helper_model()
    else:
        # there should only be one object with id=1 in helpers,
        # so check for that
        for helper in helpers:
            if helper.id != 1:
                helper.delete()

        # if there's no objects left then create one
        if len(helpers) == 0:
            _instatiate_helper_model()


def _delete_old_appointments():
    helper_object = HelperSettingsModel.objects.get(pk=1)
    last_update = helper_object.last_appointment_cleanup_time

    # set the occurance schedule to n days
    cutoff_datetime = last_update + timezone.timedelta(days=DELETE_OLD_APPOINTEMENTS_EVERY_N_DAYS)

    # only update once in awhile because 
    if timezone.now() > cutoff_datetime:

        # get the oldest 1000 appointments, sort ascending
        past_appointments = PastAppointment.objects.order_by('start_time')[:1000]

        # set max appointment age to n days
        cutoff_datetime = timezone.now() - timezone.timedelta(days=MAX_APPOINTMENT_AGE_DAYS)

        # if any of them are older than the cutoff delete them
        for appointment in past_appointments:
            if appointment.end_time < cutoff_datetime or appointment.start_time < cutoff_datetime:
                appointment.delete()

        # update the helper's last_appointment_cleanup_time
        helper_serializer = HelperSettingsSerializer(helper_object, {'last_appointment_cleanup_time': timezone.now()}, partial=True)
        helper_serializer.is_valid(raise_exception=True)
        helper_serializer.save()


def execute_helper_functions():
    _create_helper_object_if_not_exits()
    _move_completed_appointments_to_past_appointments() # not async because don't want to return an appointments view with old appointments
    sync_to_async(_delete_old_appointments(), thread_sensitive=True)