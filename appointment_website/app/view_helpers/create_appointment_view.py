from django.utils import timezone
from django.shortcuts import redirect

from ..forms import EmployeeAppointmentForm, CustomerAppointmentForm
from ..helpers import APPOINTMENT_LENGTH_MINTUES, get_groups_for_user, post_or_put_json_to_api

def get_request(class_instance, request):
    user_groups = get_groups_for_user(request.user) 

    # class_instance.context['user_is_customer'] is True by default
    class_instance.context['user_is_customer'] = True
    if 'Employees' in user_groups:
        class_instance.context['user_is_customer'] = False

    class_instance.context['form'] = EmployeeAppointmentForm() if class_instance.context['user_is_customer'] is False else CustomerAppointmentForm()

    # print('\n\Groups:\n', user_groups, '\n\n')
    # print('\n\nContext:\n', class_instance.context, '\n\n')

    return class_instance, request

def post_or_put_request(class_instance, request, put_request_id=None):
    redirect_page = ''
    try:
        form = None
        if class_instance.context['user_is_customer'] is False:
            form = EmployeeAppointmentForm(request.POST)
        else:
            form = CustomerAppointmentForm(request.POST)

        if form.is_valid():
            
            # print('\n\nCleaned Data:\n', form.cleaned_data, '\n\n')

            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']
            appointment_start_time = timezone.datetime(appointment_date.year, appointment_date.month, appointment_date.day,
                                                    appointment_time.hour, appointment_time.minute, appointment_time.second)
            appointment_end_time = appointment_start_time + timezone.timedelta(minutes=APPOINTMENT_LENGTH_MINTUES)

            customer = None
            if class_instance.context['user_is_customer'] is False:
                customer = form.cleaned_data['customer']
            else:
                customer = request.user
            
            appointment_object = {
                'start_time': appointment_start_time,
                'end_time': appointment_end_time,
                'employee_id': form.cleaned_data['employee'].id,
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
            print(f'\n\nFORM NOT VALID\n{form.errors}\n\n')
            class_instance.context['error_message'] = f'Invalid form: {form.errors.as_text}'

    except Exception as e:
        print(f'ERROR MAKING APPOINTMENT: {e}')

        class_instance.context['error_message'] = 'Unable to save appointment at this time.'

    return class_instance, request, redirect_page