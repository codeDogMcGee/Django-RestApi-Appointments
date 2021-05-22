from rest_framework import serializers
from .models import Appointment
from django.contrib.auth.models import User


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='appointment-highlight', format='html')

    class Meta:
        model = Appointment
        fields = [
            'url', 'id', 'highlight', 'owner', 'customer_name', 'employee_name',
            'appointment_datetime', 'linenos', 'language', 'style'
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    appointments = serializers.HyperlinkedRelatedField(many=True, view_name='appointment-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'appointments']


# class AppointmentSerializer(serializers.Serializer):
#     class Meta:
#         model = Appointment
#         fields = ['id', 'employee_name', 'customer_name', 'appointment_datetime']


# class AppointmentSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     customer_name = serializers.CharField(required=True, allow_blank=False, max_length=50)
#     employee_name = serializers.CharField(required=True, allow_blank=False, max_length=50)
#     appointment_datetime = serializers.DateTimeField(required=True, allow_null=False)
#     owner = serializers.ReadOnlyField(source='owner.username')  # same as CharField(read_only=True)
#
#     def create(self, validated_data):
#         return Appointment.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.customer_name = validated_data.get('customer_name')
#         instance.employee_name = validated_data.get('employee_name')
#         instance.appointment_datetime = validated_data.get('appointment_datetime')
#         instance.save()
#         return instance
#
# class UserSerializer(serializers.ModelSerializer):
#     appointments = serializers.PrimaryKeyRelatedField(many=True, queryset=Appointment.objects.all())
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'appointments']
