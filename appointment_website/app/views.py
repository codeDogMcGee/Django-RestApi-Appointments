import requests
import json
from django.shortcuts import render

from . import api_auth

from time import sleep

API_TOKEN = api_auth.get_api_token()
API_MAIN_ROUTE = 'http://127.0.0.1:8080/'

def index(request):
    return render(request, 'app/index.html')

def appointments_list(request):
    
    json_response = get_json_from_api('appointments')
    appointments_status = json_response['status']
    appointments_content = json_response['content']['results']

    # pull down all of the employees in one call since they will are all likely to be used
    # and it's assumed there aren't hundreds of thousands of employees makeing appointments
    json_response = get_json_from_api('employees')
    employees_status = json_response['status']
    employees_content = json_response['content']['results']

    for appointment in appointments_content:
        # add new elements to each appointment object with foreign key info
        
        # get employee's first name
        appointment_employee_url = appointment['employee']
        employee_first_name = 'EMPLOYEE NAME NOT FOUND'
        if employees_status == 200:
            for employee in employees_content:
                if employee['url'] == appointment_employee_url:
                    employee_first_name = employee['first_name']
                    break
        appointment['employee_first_name'] = employee_first_name

        # get employee's first name
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

def get_json_from_api(url_endpoint):
    response = {}
    try:
        url_endpoint = url_endpoint + '/' if url_endpoint[-1] != '/' else url_endpoint
        request_url = f'{API_MAIN_ROUTE}{url_endpoint}'
        print(request_url)
        response = requests.get(request_url, headers={'Authorization': f'token {API_TOKEN}'})
    except Exception as e:
        raise e

    if response == {}:
        output = {'status': 404, 'content': {}}
    else:    
        response_code = response.status_code
        response_content = response.content.decode('utf-8')  # first convert the data from bytes to text
        print(response_code, response_content)
        response_content = json.loads(response_content)  # then convert the text to json
        output = {'status': response_code, 'content': response_content}
    return output

