from django.core.validators import MinLengthValidator
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework import exceptions

from api.models import Appointment, GroupIdsModel, PastAppointment, HelperSettingsModel, ApiUser
from api.validators import prevent_double_book, is_valid_password, is_int


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
        fields = ['id', 'phone', 'name']

class AppUserNoPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiUser
        fields = ['id', 'name']


class AppCreateUserSerializer(serializers.ModelSerializer):
    password_submitted = serializers.CharField(max_length=100, validators=[is_valid_password.validate])

    class Meta:
        model = ApiUser
        fields = ['id', 'phone', 'name', 'password_submitted']


class AuthTokenSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=10, validators=[is_int.validate, MinLengthValidator(10)])
    password = serializers.CharField(required=True, max_length=100)

    def validate(self, data):
        phone = data.get('phone', None)
        password = data.get('password', None)

        user = authenticate(username=phone, password=password)

        full_user = ApiUser.objects.get(pk=user.pk)
        groups = full_user.groups.all()
        assert len(groups) == 1, 'Each user should only be in one group.'
        group_name = groups[0].name

        if user is None:
            raise exceptions.AuthenticationFailed('Incorrect phone number and/or password.')
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return {
                'token': token.key,
                'user_group': group_name
            }
