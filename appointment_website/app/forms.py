from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelChoiceField
from django.db.models import Q

from .models import CustomUser
from .helpers.helpers import format_phone_number, get_appointment_times, VALID_DATE_INPUT_FORMATS, USER_GROUPS


class CustomerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj: CustomUser) -> str:
        return super().label_from_instance(f'{obj.name} | {format_phone_number(obj.phone)}')


# class CustomerSearchField(Model)


class EmployeeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj: CustomUser) -> str:
        return super().label_from_instance(f'{obj.name}')


class CustomerAppointmentForm(forms.Form):
    employee = EmployeeChoiceField(queryset=CustomUser.objects.filter(group__name=USER_GROUPS['employees']), 
                                   widget=forms.Select, 
                                   required=True,
                                   empty_label='Select')
    appointment_date = forms.DateField(
        label='Date', 
        input_formats=VALID_DATE_INPUT_FORMATS,
        widget = forms.DateInput(attrs={'class': 'datepicker', 'is_required': 'True', 'id':'datepicker-1'}),
        required=True
    )
    appointment_time = forms.TimeField(label='Time', widget=forms.Select(choices=get_appointment_times()), required=True)  


class EmployeeAppointmentForm(forms.Form):

    def __init__(self, *args, **kwargs):
        search_text = kwargs.pop('search_text', None)
        self.n_query_results = 0
        super(EmployeeAppointmentForm, self).__init__(*args, **kwargs)

        print('\n\nSearch text:\n', search_text, '\n\n')
        
        if search_text:
            q_set = CustomUser.objects.filter(group__name=USER_GROUPS['customers']).filter(Q(name__icontains=search_text) | Q(phone__icontains=search_text))
            self.fields['customer'].queryset = q_set



            if len(q_set) > 0:
                self.fields['customer'].initial = q_set[0]
                self.n_query_results = len(q_set)
  
    customer = CustomerChoiceField(queryset=None, 
                                widget=forms.Select, 
                                required=True,
                                empty_label='Select')

    appointment_date = forms.DateField(
        label='Date', 
        input_formats=VALID_DATE_INPUT_FORMATS,
        widget=forms.DateInput(attrs={'class': 'datepicker', 'is_required': 'True', 'id':'datepicker-1'}),
        required=True
    )
    
    appointment_time = forms.TimeField(label='Time', widget=forms.Select(choices=get_appointment_times()), required=True)  


class SearchCustomerForm(forms.Form):
    search_text = forms.CharField(label='Search Customer', max_length=50, min_length=1, required=True)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'name', 'group',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'name', 'group',)


# class AppointmentDeleteButtonForm(forms.Form):
#     appointment_id = forms.IntegerField(required=True)