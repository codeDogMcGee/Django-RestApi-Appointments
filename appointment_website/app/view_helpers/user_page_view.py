from collections import OrderedDict
from django.shortcuts import redirect
from django.utils import dateparse
from django.utils.formats import date_format, time_format

from ..helpers import get_json_from_api, delete_api_object, get_groups_for_user
from ..models import CustomUser

def post_request(class_instance, request):
    request_post_query_dict = request.POST
    if 'delete_appointment_id' in request_post_query_dict.keys():
        appointment_id = request_post_query_dict['delete_appointment_id']
        try:
            appointment_id = int(appointment_id)
        except:
            appointment_id = -1

        # the database should be zero indexed
        if appointment_id > 0:
            endpoint_url = f'appointment/{appointment_id}/'
            response_object = delete_api_object(endpoint_url)
            if response_object['status'] == 204:
                # remove the deleted appointment from the context
                deleted_appointment = class_instance.context['appointments'].pop(appointment_id)
                print('Deleted Appointment', deleted_appointment)
            else:
                class_instance.context['error_message'] = 'Can not delete appointment at this time'


    return class_instance, request

def get_request(class_instance, request):
    user_groups = get_groups_for_user(request.user)
        
    url_endpoint = ''
    if 'Employees' in user_groups:
        url_endpoint = 'appointments-employee/'
    elif 'Customers' in user_groups:
        url_endpoint = 'appointments-customer/'
    
    appointments_dict = OrderedDict()
    if len(url_endpoint) > 0:    
        # attach the id to the end of the endpoint before sending
        url_endpoint += str(request.user.id)
        api_response = get_json_from_api(url_endpoint)
        if api_response['status'] == 200:
            appointments_list = api_response['content']

            class_instance.context['last_appointment_id'] = appointments_list[-1]['id']

            for appointment in appointments_list:
                # format appointment start data and time
                try:
                    start_datetime = dateparse.parse_datetime(appointment['start_time'])
                    start_time = time_format(start_datetime.time(), 'P')
                    start_date = date_format(start_datetime.date(), 'D M j')

                    appointment['start_time_string'] = f'{start_date} at {start_time}'
                except:
                    print('Error parsing datetime string from API', appointment['start_time'])
                    appointment['start_time_string'] = ''

                # attach other user name to appointment
                if 'Employees' in user_groups:
                    other_user_id = appointment['customer_id']
                else:
                    other_user_id = appointment['employee_id']

                other_user = CustomUser.objects.get(pk=other_user_id)
                appointment['other_user'] = other_user

                # attach edit and delete action urls
                appointment['action_url_delete'] = f''

                appointments_dict[appointment['id']] = appointment
    
    class_instance.context['appointments'] = appointments_dict
    class_instance.context['user_name'] = request.user.name

    return class_instance, request