from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelChoiceField

from .models import CustomUser
from .helpers import format_phone_number, get_appointment_times, MAIN_DATE_FORMAT


class CustomerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj: CustomUser) -> str:
        return super().label_from_instance(f'{obj.name} | {format_phone_number(obj.phone)}')


class EmployeeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj: CustomUser) -> str:
        return super().label_from_instance(f'{obj.name}')


class CustomerAppointmentForm(forms.Form):
    employee = EmployeeChoiceField(queryset=CustomUser.objects.filter(group__name='Employees'), 
                                   widget=forms.Select, 
                                   required=True)
    appointment_date = forms.DateField(
        label='Date', 
        input_formats=['%m/%d/%Y', '%m-%d-%Y'],
        widget = forms.DateInput(attrs={'class': 'datepicker', 'is_required': 'True', 'id':'datepicker-1'})
    )
    appointment_time = forms.TimeField(label='Time', widget=forms.Select(choices=get_appointment_times()))  


class EmployeeAppointmentForm(CustomerAppointmentForm):
    customer = CustomerChoiceField(queryset=CustomUser.objects.filter(group__name='Customers'), 
                                   widget=forms.Select, 
                                   required=True)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'email', 'name', 'group',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'email', 'name', 'group',)


# class AppointmentDeleteButtonForm(forms.Form):
#     appointment_id = forms.IntegerField(required=True)