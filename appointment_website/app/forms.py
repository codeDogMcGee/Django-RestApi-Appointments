from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelChoiceField
from django.utils import timezone
from django.utils.formats import time_format

from .models import CustomUser
from .helpers import format_phone_number, APPOINTMENT_LENGTH_MINTUES
    

def get_appointment_times():
    start_time = timezone.datetime(2000,1,1,7,0,0)
    end_time = timezone.datetime(2000,1,1,18,30,0)

    output = []
    _time = start_time
    while _time <= end_time:
        output.append((_time, time_format(_time, 'h:i a')))
        _time += timezone.timedelta(minutes=APPOINTMENT_LENGTH_MINTUES)
    # return a tuple used by forms.Select (drop-down) in a format of (key, value)
    return output


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
        input_formats=['%m/%d/%Y'], #  %H:%M
        widget = forms.DateInput(attrs={'class': 'datepicker', 'is_required': 'True', 'id':'datepicker-1'})
    )
    appointment_time = forms.DateTimeField(label='Time', widget=forms.Select(choices=get_appointment_times()))  

class EmployeeAppointmentForm(CustomerAppointmentForm):
    customer = CustomerChoiceField(queryset=CustomUser.objects.filter(group__name='Customers'), widget=forms.Select, required=True)

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('phone', 'email', 'name', 'group',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('phone', 'email', 'name', 'group',)