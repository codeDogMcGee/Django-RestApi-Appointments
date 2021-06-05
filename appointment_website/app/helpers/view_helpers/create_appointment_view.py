from django.db.models import Q
from django.utils import timezone
from django.shortcuts import redirect
import traceback

from app.models import CustomUser
from app.forms import EmployeeAppointmentForm, CustomerAppointmentForm, SearchCustomerForm
from app.helpers.helpers import APPOINTMENT_LENGTH_MINTUES, post_or_put_json_to_api
from app.helpers.user_helpers import get_groups_for_user


def get_request(class_instance, request):
    # initialize attributes
    class_instance.context['error_message'] = ''

    # class_instance.context['user_is_customer'] is True by default
    class_instance.context['user_is_customer'] = True
    if 'Employees' in get_groups_for_user(request.user):
        class_instance.context['user_is_customer'] = False

    # display appropriate form based on user groups
    if class_instance.context['user_is_customer'] is False:
        class_instance.context['search_customer_form'] = SearchCustomerForm()
        class_instance.context['appointment_form'] = None
        class_instance.context['search_text'] = ''

    else:
         class_instance.context['appointment_form'] = CustomerAppointmentForm(initial={'date': timezone.now})

    return class_instance, request

def post_or_put_request(class_instance, request, put_request_id=None):
    redirect_page = ''
    class_instance.context['error_message'] = ''

    print('\n\nForm POST:\n', request.POST, '\n')

    if 'search_text' in request.POST.keys():
        try:
            form = SearchCustomerForm(request.POST)
            if form.is_valid():
                user_search_text = form.cleaned_data['search_text']
                
                class_instance.context['appointment_form'] = EmployeeAppointmentForm(search_text=user_search_text, initial={'appointment_date': timezone.now().date()})

                # class_instance.context['search_text'] = user_search_text
                print('\n\nNow Date:', timezone.now().date(), '\n\n')

                class_instance.context['search_text'] = user_search_text


            else:
                print(f'\n\nSEARCH FORM NOT VALID\n{form.errors}\n\n')
                class_instance.context['error_message'] = f'Invalid customer search form: {form.errors.as_text}'

        except Exception as e:
            print(f'ERROR IN SEARCH: {e}')
            class_instance.context['error_message'] = 'Unable to search for customer at this time.'

    else:
        try:
            form = None
            if class_instance.context['user_is_customer'] is False:
                form = EmployeeAppointmentForm(request.POST, search_text=class_instance.context['search_text'])
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
                if class_instance.context['user_is_customer'] is False:
                    customer = form.cleaned_data['customer']
                    employee = request.user
                else:
                    customer = request.user
                    employee = form.cleaned_data['employee']
                
                appointment_object = {
                    'start_time': appointment_start_time,
                    'end_time': appointment_end_time,
                    'employee_id': employee.id,
                    'customer_id': customer.id
                }

                response_object = {}
                if put_request_id:
                    appointment_object['id'] = put_request_id
                    response_object = post_or_put_json_to_api('PUT', f'appointment/{put_request_id}/', appointment_object)
                else:
                    # post the new appointment to the api db
                    response_object = post_or_put_json_to_api('POST', 'appointments', appointment_object)

                if response_object['status'] == 201 or response_object['status'] == 200:  
                    # return redirect('user-page') 
                    redirect_page = 'user-page'   
                
                else:
                    print('\n\nERROR CREATING APPOINTMENT:\n', f'status={response_object["status"]}, message={response_object["content"]}')
                    
                    class_instance.context['error_message'] = response_object["content"]
                

            else:
                print(f'\n\nAPPOINTMENT FORM NOT VALID\n{form.errors}\n\n')
                class_instance.context['error_message'] = f'Invalid appointment form: {form.errors.as_text}'

        except Exception:
            print(f'ERROR MAKING APPOINTMENT: {traceback.format_exc()}')

            class_instance.context['error_message'] = 'Unable to save appointment at this time.'

    return class_instance, request, redirect_page