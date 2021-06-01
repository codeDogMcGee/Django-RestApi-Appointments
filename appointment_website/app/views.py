from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, response
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from app.forms import CustomUserCreationForm, CustomUserChangeForm, CustomerAppointmentForm, EmployeeAppointmentForm
from django.contrib.auth.models import Group
from django.utils import timezone, dateparse
from django.utils.formats import date_format, time_format
from django.shortcuts import redirect, render

from .helpers import get_json_from_api, post_json_to_api, APPOINTMENT_LENGTH_MINTUES, get_groups_for_user
from .models import CustomUser


def index(request):
    return render(request, 'app/index.html')


class UserPageView(LoginRequiredMixin, View):
    template_name = 'app/user-page.html'
    login_url = '/login/'

    context = {
        'user_name': '', 
        'appointments': [],
        'error_message': ''
    }

    def get(self, request):
        user_groups = get_groups_for_user(request.user)
        
        url_endpoint = ''
        if 'Employees' in user_groups:
            url_endpoint = 'appointments-employee/'
        elif 'Customers' in user_groups:
            url_endpoint = 'appointments-customer/'
        
        appointments = []
        if len(url_endpoint) > 0:    
            # attach the id to the end of the endpoint before sending
            url_endpoint += str(request.user.id)
            api_response = get_json_from_api(url_endpoint)
            if api_response['status'] == 200:
                appointments = api_response['content']

                # attach other user name to appointment
                # also break up appointment start data and time
                for appointment in appointments:

                    try:
                        start_datetime = dateparse.parse_datetime(appointment['start_time'])
                        start_time = time_format(start_datetime.time(), 'P')
                        start_date = date_format(start_datetime.date(), 'D M j')

                        appointment['start_time_string'] = f'{start_date} at {start_time}'
                    except:
                        print('Error parsing datetime string from API', appointment['start_time'])
                        appointment['start_time_string'] = ''


                    if 'Employees' in user_groups:
                        other_user_id = appointment['customer_id']
                    else:
                        other_user_id = appointment['employee_id']

                    other_user = CustomUser.objects.get(pk=other_user_id)
                    appointment['other_user'] = other_user
        
        self.context['appointments'] = appointments
        self.context['user_name'] = request.user.name

        print('\n\nContext:\n', self.context, '\n\n')

        return render(request, self.template_name, self.context)


class CreateAppointmentView(LoginRequiredMixin, View):
    template_name = 'app/make-appointment.html'
    login_url = '/login/'

    context = {
        'form': None,
        'user_is_customer': True,
        'appointment_start_time': '',
        'error_message': ''
    }

    def get(self, request):

        user_groups = get_groups_for_user(request.user) 

        # self.context['user_is_customer'] = True by default
        if 'Customers' not in user_groups and 'Employees' in user_groups:
            self.context['user_is_customer'] = False

        self.context['form'] = EmployeeAppointmentForm() if self.context['user_is_customer'] is False else CustomerAppointmentForm()

        return render(request, self.template_name, self.context)

    def post(self, request):
        try:
            form = None
            if self.context['user_is_customer'] is False:
                form = EmployeeAppointmentForm(request.POST)
            else:
                form = CustomerAppointmentForm(request.POST)

            if form.is_valid():
                
                print('\n\nCleaned Data:\n', form.cleaned_data, '\n\n')

                appointment_date = form.cleaned_data['appointment_date']
                appointment_time = form.cleaned_data['appointment_time']
                appointment_start_time = timezone.datetime(appointment_date.year, appointment_date.month, appointment_date.day,
                                                        appointment_time.hour, appointment_time.minute, appointment_time.second)
                appointment_end_time = appointment_start_time + timezone.timedelta(minutes=APPOINTMENT_LENGTH_MINTUES)

                customer = None
                if self.context['user_is_customer'] is False:
                    customer = form.cleaned_data['customer']
                else:
                    customer = request.user
                
                appointment_object = {
                    'start_time': appointment_start_time,
                    'end_time': appointment_end_time,
                    'employee_id': form.cleaned_data['employee'].id,
                    'customer_id': customer.id
                }

                # post the new appointment to the api db
                response_object = post_json_to_api('appointments', appointment_object)

                if response_object['status'] == 201:  
                    return redirect('/user-page/')    
                else:
                    print('\n\nERROR CREATING APPOINTMENT:\n', f'status={response_object["status"]}, message={response_object["content"]}')
                    
                    self.context['error_message'] = response_object["content"]
                

            else:
                print(f'\n\nFORM NOT VALID\n{form.errors}\n\n')

        except Exception as e:
            print(f'ERROR MAKING APPOINTMENT: {e}')

            self.context['error_message'] = 'Unable to save appointment at this time.'

        return render(request, self.template_name, self.context)


def appointments_list(request):
    
    # get all appointments from the api
    json_response = get_json_from_api('appointments')

    print('\n\nAPPOINTMENTS:\n', json_response['status'], json_response['content'], '\n\n')

    appointments_status = json_response['status']
    appointments_content = json_response['content']

    for appointment in appointments_content:

        # format appointment start time
        start_datetime = dateparse.parse_datetime(appointment['start_time'])
        start_time = time_format(start_datetime.time(), 'P')
        start_date = date_format(start_datetime.date(), 'D M n')
        appointment['start_time'] = f'{start_date} @ {start_time}'
        
        # format appointment end time
        end_datetime = dateparse.parse_datetime(appointment['end_time'])
        end_time = time_format(end_datetime.time(), 'P')
        end_date = date_format(end_datetime.date(), 'D M n')
        appointment['end_time'] = f'{end_date} @ {end_time}'
        
        # use the appointment employee_id to find the employee in CustomUser
        appointment['employee'] = CustomUser.objects.get(pk=appointment['employee_id'])

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