from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from app.forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import Group
from django.utils import dateparse
from django.utils.formats import date_format, time_format
from django.shortcuts import redirect, render
from collections import OrderedDict

from .helpers.helpers import get_json_from_api, initialize_groups
from .helpers.view_helpers import user_page_view, create_appointment_view, appointment_detail_view
from .models import CustomUser


def index(request):
    return render(request, 'app/index.html')


class UserPageView(LoginRequiredMixin, View):
    template_name = 'app/user-page.html'
    login_url = '/login/'

    context = {
        'user_name': '', 
        'appointments': OrderedDict(),
        'last_appointment_id': None,
        'error_message': ''
    }

    def get(self, request):
        self, request = user_page_view.get_request(self, request)
        return render(request, self.template_name, self.context)

    def post(self, request):
        self, request = user_page_view.post_request(self, request)
        # if redirect_url != '':
        #     redirect(redirect_url)
        return render(request, self.template_name, self.context)


class CreateAppointmentView(LoginRequiredMixin, View):
    template_name = 'app/make-appointment.html'
    login_url = '/login/'
    context = {    
        'appointment_form': None,
        'search_user_form': None,
        'search_text': '',
        # 'n_search_results': -1, 
        # 'search_result_query_set': None,
        # 'search_text': '',
        # 'temp': '',

        'user_is_customer': True,
        'page_header': 'Make an Appointment',
        'submit_button_text': 'Schedule',
        'submit_method_type': 'post',
        'error_message': ''
    }

    def get(self, request):
        self, request = create_appointment_view.get_request(self, request)
        return render(request, self.template_name, self.context)

    def post(self, request):
        self, request, redirect_page = create_appointment_view.post_or_put_request(self, request)
        # if redirect_page != '':
        #     return redirect(redirect_page)
        return render(request, self.template_name, self.context)


class AppointmentDetailView(LoginRequiredMixin, View):
    """
    This class uses the same html template as CreateAppointmentView(),
    so the same context properties are needed, except appointment_id is added here.
    """
    template_name = 'app/make-appointment.html'
    login_url = '/login/'
    context = {    
        'appointment_form': None,
        'search_user_form': None,
        'user_search_text': '',

        'appointment_id': -1,
        'user_is_customer': True,
        'page_header': 'Change Appointment',
        'submit_button_text': 'Change',
        'submit_method_type': 'put',
        'error_message': ''
    }

    def get(self, request, pk):
        self, request = appointment_detail_view.get_request(self, request, pk)
        return render(request, self.template_name, self.context)

    def post(self, request, pk):
        """
        This post is actually a put that uses the same method 
        as CreateAppointmentView post, but with a 'PUT' flag
        """
        self, request, redirect_page = create_appointment_view.post_or_put_request(self, request, pk)
        if redirect_page != '':
            return redirect(redirect_page)
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
    # Initialize the groups to make sure they are present, don't need the output
    _ = initialize_groups()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            form.save()

            print('\n\nCleaned Data:\n', form.cleaned_data, '\n\n')


            authenticate(
                phone = form.cleaned_data['phone'], 
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

