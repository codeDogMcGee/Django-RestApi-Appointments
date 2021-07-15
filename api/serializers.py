from django.core.validators import MinLengthValidator
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework import exceptions

from api.models import Appointment, EmployeeScheduleModel, GroupIdsModel, PastAppointment, HelperSettingsModel, ApiUser, ServiceMenuModel, EmailVerificationToken
from api.validators import prevent_double_book, appointment_fits_employee_schedule, is_valid_password, max_services_per_appointment, under_max_appointments


class AppointmentSerializer(serializers.ModelSerializer):
    
    def validate(self, appointment):
        appointment = appointment_fits_employee_schedule.validate(appointment)
        appointment = under_max_appointments.validate(appointment)
        appointment = prevent_double_book.validate(appointment)
        appointment = max_services_per_appointment.validate(appointment)
        return appointment

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
        fields = ['id', 'email', 'name', 'phone']

class AppUserNameOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiUser
        fields = ['id', 'name']

class AppUserEmailAndPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiUser
        fields = ['id', 'email', 'phone']


class AppUserWithGroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiUser
        fields = ['id', 'email', 'phone', 'name', 'groups']


class AppCreateUserSerializer(serializers.ModelSerializer):
    password_submitted = serializers.CharField(max_length=100, validators=[is_valid_password.validate])

    class Meta:
        model = ApiUser
        fields = ['id', 'email', 'name', 'phone', 'password_submitted']


class AppUserChangePasswordSerializer(serializers.ModelSerializer):
    password_submitted = serializers.CharField(max_length=100, validators=[is_valid_password.validate])

    class Meta:
        model = ApiUser
        fields = ['id', 'email', 'password_submitted']


class ServiceMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceMenuModel
        fields = '__all__'


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeScheduleModel
        fields = '__all__'


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed('Incorrect email and/or password.')
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return {
                'token': token.key
            }

class EmailVerificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationToken
        fields = '__all__'
