from rest_framework import serializers

from api.models import Appointment, GroupIdsModel, PastAppointment, HelperSettingsModel, ApiUser
from api.validators import prevent_double_book, is_valid_password


class AppointmentSerializer(serializers.ModelSerializer):
    
    def validate(self, appointment):
        return prevent_double_book.validate(appointment)

    class Meta:
        model = Appointment
        fields = '__all__'
    

class PastAppointmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PastAppointment
        fields = '__all__'


class HelperSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelperSettingsModel
        fields = '__all__'


class GroupIdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupIdsModel
        fields = '__all__'


class AppUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiUser
        fields = ['id', 'phone', 'name', 'groups']


class AppCreateUserSerializer(serializers.ModelSerializer):
    password_submitted = serializers.CharField(max_length=100, validators=[is_valid_password.validate])

    class Meta:
        model = ApiUser
        fields = ['id', 'phone', 'name', 'password_submitted']