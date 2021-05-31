from django.views.decorators.csrf import csrf_protect
from app.forms import CustomUserCreationForm, CustomUserChangeForm, AppointmentForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.utils import timezone
from django.shortcuts import redirect, render

from .helpers import get_json_from_api, post_json_to_api, APPOINTMENT_LENGTH_MINTUES
from .models import CustomUser


def index(request):
    return render(request, 'app/index.html')


def make_appointment(request):
    customer_display_name = ''
    employee_display_name = ''
    appointment_display_time = ''

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            
            print('\n\nCleaned Data:\n', form.cleaned_data, '\n\n')

            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']
            appointment_start_time = timezone.datetime(appointment_date.year, appointment_date.month, appointment_date.day,
                                                       appointment_time.hour, appointment_time.minute, appointment_time.second)

            appointment_end_time = appointment_start_time + timezone.timedelta(minutes=APPOINTMENT_LENGTH_MINTUES)



            print('\n\nAPPOINTMENT TO SEND:\n', f'Employee {form.cleaned_data["employee"].id} | Customer {form.cleaned_data["customer"].id} | Start Time {appointment_start_time} | End Time {appointment_end_time}\n\n')
            
            appointment_object = {
                'start_time': appointment_start_time,
                'end_time': appointment_end_time,
                'employee_id': form.cleaned_data['employee'].id,
                'customer_id': form.cleaned_data['customer'].id
            }

            response_object = post_json_to_api('appointments', appointment_object)
            if response_object['status'] == 201:    
                customer_display_name = form.cleaned_data['customer'].name
                employee_display_name = form.cleaned_data['employee'].name
                appointment_display_time = appointment_start_time
                
            else:
                print('\n\nERROR CREATING APPOINTMENT:\n', f'status={response_object["status"]}, message={response_object["content"]}')
                redirect('make-appointment')

                
    else:
        form = AppointmentForm()

    return render(request, 'app/make-appointment.html', {'form': form, 
                                                         'customer_name': customer_display_name, 
                                                         'employee_name': employee_display_name,
                                                         'appointment_start_time': appointment_display_time
                                                         })


def appointments_list(request):
    
    # get all appointments from the api
    json_response = get_json_from_api('appointments')

    print('\n\nAPPOINTMENTS:\n', json_response['status'], json_response['content'], '\n\n')

    appointments_status = json_response['status']
    appointments_content = json_response['content']

    for appointment in appointments_content:

        # adjust format of appointement time
        start_time_list = appointment['start_time'].split('T')  # Django's timezone stamp has a T in the time we don't need
        time_string = start_time_list[-1]
        time_string = time_string[:5]
        appointment['start_time'] = ' '.join([start_time_list[0], time_string])

    context = {}
    if appointments_status == 200:
        context = {'appointments': appointments_content}

    return render(request, 'app/appointments.html', context)


@csrf_protect
def create_user(request):
    # Initialize the groups to make sure they are present
    Group.objects.get_or_create(name='Employees')
    Group.objects.get_or_create(name='Customers')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            form.save()

            print('\n\nCleaned Data:\n', form.cleaned_data, '\n\n')


            authenticate(
                phone = form.cleaned_data['phone'], 
                email = form.cleaned_data['email'], 
                name = form.cleaned_data['name'], 
                group = form.cleaned_data['group'],
                password = form.cleaned_data['password1']
            )

            return redirect('make-appointment')
    else:
        form = CustomUserCreationForm()

    return render(request, 'app/create-user.html', {'form': form})



def modify_user(request):
    # Initialize the groups to make sure they are present
    Group.objects.get_or_create(name='Employees')
    Group.objects.get_or_create(name='Customers')

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST)
        if form.is_valid():
            
            print('\n\nCleaned Data:\n', form.cleaned_data, '\n\n')
            
    else:
        form = CustomUserChangeForm()

    return render(request, 'app/modify-user.html', {'form': form})