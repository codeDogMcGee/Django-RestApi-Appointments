from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User

from api.models import Appointment, PastAppointment
from api.serializers import AppointmentSerializer, UserSerializer, PastAppointmentSerializer


def move_completed_appointments_to_past_appointments():
    appointments = Appointment.objects.all()
    for appointment in appointments:
        if timezone.now() > appointment.appointment_end_time:

            past_appointment_object = {
                'appointment_start_time' : appointment.appointment_start_time, 
                'appointment_end_time' : appointment.appointment_end_time, 
                'customer_id' : appointment.customer_id,
                'employee_id' : appointment.employee_id,
                'created' : appointment.created
            }

            past_appointment_serializer = PastAppointmentSerializer(data=past_appointment_object)
            
            # save any appointment that is completed to PastAppointments and delete from Appointments
            if past_appointment_serializer.is_valid():
                past_appointment_serializer.save()
                appointment.delete()
            else:
                print(f'\nERROR SERIALIZING DATA: {past_appointment_serializer.errors}\n')


class AppointmentList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):

        move_completed_appointments_to_past_appointments()

        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class PastAppointmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = PastAppointment.objects.all()
    serializer_class = PastAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
