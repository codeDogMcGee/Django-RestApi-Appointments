from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone
from .models import Appointment, Customer, Employee


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    is_completed = serializers.ReadOnlyField()  # source='is_completed'

    class Meta:
        model = Appointment
        fields = ['url', 'id', 'created', 'customer', 'employee', 'appointment_datetime', 'is_completed']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email']


class CustomerAdminSerializer(serializers.HyperlinkedModelSerializer):
    upcoming_appointments = serializers.SerializerMethodField('future_appointments')

    @staticmethod
    def future_appointments(this_customer):
        output = []
        query = Appointment.objects.filter(customer=this_customer).values()
        for item in query:
            if item['appointment_datetime'] > timezone.now():
                output.append(item)
        return output

    class Meta:
        model = Customer
        fields = ['url', 'id', 'created', 'first_name', 'email', 'upcoming_appointments']  # , 'last_appointment_date']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    upcoming_appointments = serializers.SerializerMethodField('future_appointments')
    last_appointment = serializers.SerializerMethodField('most_recent_appointment')

    @staticmethod
    def future_appointments(this_customer):
        output = []
        query = Appointment.objects.filter(customer=this_customer)\
                                    .filter(appointment_datetime__gt=timezone.now())\
                                    .order_by('appointment_datetime')\
                                    .values()
        for item in query:
            print(item)
            if item['appointment_datetime'] > timezone.now():
                output.append(item)
        return query

    @staticmethod
    def most_recent_appointment(this_customer):
        query = Appointment.objects.filter(customer=this_customer)\
                                    .filter(appointment_datetime__lt=timezone.now())\
                                    .order_by('-appointment_datetime')\
                                    .values()
        return query[0] if len(query) > 0 else []

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'email', 'upcoming_appointments', 'last_appointment']


class EmployeeAdminSerializer(serializers.HyperlinkedModelSerializer):
    upcoming_appointments = serializers.SerializerMethodField('future_appointments')

    @staticmethod
    def future_appointments(this_employee):
        output = []
        query = Appointment.objects.filter(employee=this_employee).values()
        for item in query:
            if item['appointment_datetime'] > timezone.now():
                output.append(item)
        return output

    class Meta:
        model = Employee
        fields = ['url', 'id', 'created', 'first_name', 'email', 'upcoming_appointments']


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    upcoming_appointments = serializers.SerializerMethodField('future_appointments')

    @staticmethod
    def future_appointments(this_employee):
        output = []
        query = Appointment.objects.filter(employee=this_employee).values()
        for item in query:
            if item['appointment_datetime'] > timezone.now():
                output.append(item)
        return output

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'email', 'upcoming_appointments']
