from django.utils import dateparse
from django.utils.formats import date_format

from app.models import CustomUser
from app.forms import EmployeeAppointmentForm, CustomerAppointmentForm
from app.helpers.helpers import get_json_from_api, MAIN_DATE_FORMAT
from app.helpers.user_helpers import get_groups_for_user


def get_request(class_instance, request, pk):

    initial_appointment_values = {}

    user_groups = get_groups_for_user(request.user) 
    # class_instance.context['user_is_customer'] is True by default
    class_instance.context['user_is_customer'] = True
    if 'Employees' in user_groups:
        class_instance.context['user_is_customer'] = False


    api_response = get_json_from_api(f'appointment/{pk}')

    print('\n\nAPI Repsonse:\n', api_response, '\n\n')

    if api_response['status'] == 200:

        appointment = api_response['content']

        appointment_datetime = dateparse.parse_datetime(appointment['start_time'])

        employee = CustomUser.objects.get(pk=appointment['employee_id'])

        print('\nemployee:', employee,'\n')

        initial_appointment_values = {
            'employee': employee.id,
            'appointment_date': date_format(appointment_datetime.date(), MAIN_DATE_FORMAT),
            'appointment_time': appointment_datetime.time()
        }

        class_instance.context['appointment_id'] = appointment['id']

    form = None
    if class_instance.context['user_is_customer']:
        form = CustomerAppointmentForm(initial=initial_appointment_values)
    else:
        initial_appointment_values['customer'] = CustomUser.objects.filter(pk=appointment['customer_id'])
        form = EmployeeAppointmentForm(initial=initial_appointment_values)

    class_instance.context['form'] = form

    return class_instance, request