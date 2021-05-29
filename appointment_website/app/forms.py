from django.db import models
from django import forms
import datetime

from .helpers import get_json_from_api


def get_employees():
    json_response = get_json_from_api('employees')
    employees_status = json_response['status']
    employees_content = json_response['content']['results']

    output = []
    if employees_status == 200:
        output = employees_content
        output = [(employee['url'], employee['first_name']) for employee in employees_content]
    # return a tuple used by forms.Select (drop-down) in a format of (key, value)
    return output

def get_times():
    start_time = datetime.datetime(1,1,1,7,0,0)
    end_time = datetime.datetime(1,1,1,18,30,0)
    appointment_length_minutes = 30

    output = []
    _time = start_time
    while _time <= end_time:
        output.append((_time, datetime.datetime.strftime(_time, '%I:%M %p')))
        _time += datetime.timedelta(minutes=appointment_length_minutes)
    # return a tuple used by forms.Select (drop-down) in a format of (key, value)
    return output

class NameForm(forms.Form):
    customer_first_name = forms.CharField(label='First name', max_length=100)
    appointment_date = forms.DateField(
        label='Date', 
        input_formats=['%m/%d/%Y'], #  %H:%M
        widget = forms.DateInput(attrs={'class': 'datepicker', 'is_required': 'True', 'id':'datepicker-1'})
    )
    appointment_time = forms.CharField(label='Time', widget=forms.Select(choices=get_times()))
    employee = forms.CharField(label='Nail Artist', widget=forms.Select(choices=get_employees()))