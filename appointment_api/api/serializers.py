from rest_framework import serializers
from .models import Appointment, Customer, Employee
from django.contrib.auth.models import User


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_completed = serializers.ReadOnlyField()  # source='is_completed'

    class Meta:
        model = Appointment
        fields = ['url', 'id', 'owner', 'customer', 'employee', 'appointment_datetime', 'is_completed']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    appointments = serializers.HyperlinkedRelatedField(many=True, view_name='appointment-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'appointments']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Customer
        fields = ['url', 'id', 'owner', 'first_name', 'last_name', 'email', 'phone', 'last_appointment_date']


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ['url', 'id', 'user', 'email', 'phone']