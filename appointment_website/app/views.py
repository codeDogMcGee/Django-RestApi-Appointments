from app.forms import AppointmentForm
from datetime import datetime
from django.shortcuts import render

from .helpers import get_json_from_api, API_MAIN_ROUTE


def index(request):
    return render(request, 'app/index.html')


def make_appointment(request):

    customer_first_name = ''
    appointment_datetime = ''
    employee = ''

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            
            print('\n\nCleaned Data:\n', form.cleaned_data, '\n\n')
            
            customer_first_name = form.cleaned_data['customer_first_name']
            appointment_date = form.cleaned_data['appointment_date']
            
            appointment_time = form.cleaned_data['appointment_time']
            appointment_time = datetime.strptime(appointment_time, '%Y-%m-%d %H:%M:%S')

            appointment_datetime = datetime(appointment_date.year, appointment_date.month, appointment_date.day,
                                            appointment_time.hour, appointment_time.minute, appointment_time.second)

            endpoint = form.cleaned_data['employee']
            endpoint = endpoint.replace(API_MAIN_ROUTE, '') 

            employee_content_object = get_json_from_api(endpoint)
            employee_status = employee_content_object['status']
            employee_content = employee_content_object['content']

            employee = 'EMPLOYEE NOT FOUND'
            if employee_status == 200 and len(employee_content) > 0:
                employee = employee_content['first_name']
            
    else:
        form = AppointmentForm()

    return render(request, 'app/make-appointment.html', {'form': form, 
                                                         'customer_first_name': customer_first_name, 
                                                         'appointment_datetime': appointment_datetime,
                                                         'employee': employee
                                                         })


def appointments_list(request):
    
    # get all appointments from the api
    json_response = get_json_from_api('appointments')
    appointments_status = json_response['status']
    appointments_content = json_response['content']['results']

    # pull down all of the employees in one call since they are all likely to be used
    # and it's assumed there aren't hundreds of thousands of employees making appointments,
    # which would could be too big an object to pull through the api
    json_response = get_json_from_api('employees')
    employees_status = json_response['status']
    employees_content = json_response['content']['results']

    for appointment in appointments_content:

        # adjust format of appointement time
        date_time_list = appointment['appointment_datetime'].split('T')  # Django's timezone stamp has a T in the time we don't need
        time_string = date_time_list[-1]
        time_string = time_string[:5]
        appointment['appointment_datetime'] = ' '.join([date_time_list[0], time_string])

        ### add new elements to each appointment object with foreign key info        
        # get employee's first name
        appointment_employee_url = appointment['employee']
        employee_first_name = 'EMPLOYEE NAME NOT FOUND'
        if employees_status == 200:
            for employee in employees_content:
                if employee['url'] == appointment_employee_url:
                    employee_first_name = employee['first_name']
                    break
        appointment['employee_first_name'] = employee_first_name

        # get customer's first name
        # we make a call to the api each time since to avoid pulling too much data over the api
        # since we don't know how many customers there might be
        endpoint = appointment['customer'].replace(API_MAIN_ROUTE, '') 
        customer_content_object = get_json_from_api(endpoint)
        customer_status = customer_content_object['status']
        customer_content = customer_content_object['content']
        if customer_status == 200 and len(customer_content) > 0:
            appointment['customer_first_name'] = customer_content['first_name']
        else:
            appointment['customer_first_name'] = 'CUSTOMER NAME NOT FOUND'

    context = {}
    if appointments_status == 200:
        context = {'appointments': appointments_content}

    return render(request, 'app/appointments.html', context)

