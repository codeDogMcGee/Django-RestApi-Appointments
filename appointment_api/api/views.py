from django.http.response import Http404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

from api.models import Appointment, HelperModel, PastAppointment
from api.serializers import AppointmentSerializer, HelperSerializer, UserSerializer, PastAppointmentSerializer


DELETE_OLD_APPOINTEMENTS_EVERY_N_DAYS = 1
MAX_APPOINTMENT_AGE_DAYS = 5


def _move_completed_appointments_to_past_appointments():
    appointments = Appointment.objects.all()
    for appointment in appointments:
        if timezone.now() > appointment.end_time:

            past_appointment_object = {
                'start_time' : appointment.start_time, 
                'end_time' : appointment.end_time, 
                'customer_id' : appointment.customer_id,
                'employee_id' : appointment.employee_id,
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
    helpers_serializer = HelperSerializer(data=helper_object)

    if helpers_serializer.is_valid():
        helpers_serializer.save()
    else:
        print(f'\nERROR INSTATIATING HELPER MODEL: {helpers_serializer.errors}\n')


def _create_helper_object_if_not_exits():
    helpers = HelperModel.objects.all()

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
    helper_object = HelperModel.objects.get(pk=1)
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
        helper_serializer = HelperSerializer(helper_object, {'last_appointment_cleanup_time': timezone.now()}, partial=True)
        helper_serializer.is_valid(raise_exception=True)
        helper_serializer.save()


def _execute_helper_functions():
    _create_helper_object_if_not_exits()
    _move_completed_appointments_to_past_appointments() # not async because don't want to return an appointments view with old appointments
    sync_to_async(_delete_old_appointments(), thread_sensitive=True)


class AppointmentList(APIView):
    """
    Read all appointments, or create new appointment
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        _execute_helper_functions()

        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetail(APIView):
    """
    Read, Update, Delete functionality for one Appointment
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_appointment(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        _execute_helper_functions()

        appointment = self.get_appointment(pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk):
        appointment = self.get_appointment(pk)
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        appointment = self.get_appointment(pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PastAppointmentList(APIView):
    """
    Read all appointments
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        _execute_helper_functions()

        appointments = PastAppointment.objects.all()
        serializer = PastAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class PastAppointmentDetail(APIView):
    """
    Read only functionality for one Appointment
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_appointment(self, pk):
        try:
            return PastAppointment.objects.get(pk=pk)
        except PastAppointment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        _execute_helper_functions()

        appointment = self.get_appointment(pk)
        serializer = PastAppointmentSerializer(appointment)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class HelpersViewSet(viewsets.ReadOnlyModelViewSet):

    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = HelperModel.objects.all()
    serializer_class = HelperSerializer
    permission_classes = [permissions.IsAdminUser]
