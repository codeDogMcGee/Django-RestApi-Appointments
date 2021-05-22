from rest_framework import serializers
from .models import Appointment


# class AppointmentSerializer(serializers.Serializer):
#     class Meta:
#         model = Appointment
#         fields = ['id', 'employee_name', 'customer_name', 'appointment_datetime']


class AppointmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    customer_name = serializers.CharField(required=True, allow_blank=False, max_length=50)
    employee_name = serializers.CharField(required=True, allow_blank=False, max_length=50)
    appointment_datetime = serializers.DateTimeField(required=True, allow_null=False)

    def create(self, validated_data):
        return Appointment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.customer_name = validated_data.get('customer_name')
        instance.employee_name = validated_data.get('employee_name')
        instance.appointment_datetime = validated_data.get('appointment_datetime')
        instance.save()
        return instance
