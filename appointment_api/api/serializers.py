from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Appointment, PastAppointment, HelperModel
from .validators import prevent_double_book

class AppointmentSerializer(serializers.ModelSerializer):
    
    def validate(self, appointment):
        return prevent_double_book(appointment)

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


class HelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelperModel
        fields = '__all__'