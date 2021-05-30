from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Appointment, PastAppointment


class AppointmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Appointment
        fields = '__all__'
    

class PastAppointmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PastAppointment
        fields = '__all__'
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']
