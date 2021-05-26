import requests
import json
from django.shortcuts import render

from . import api_auth

API_TOKEN = api_auth.get_api_token()
API_MAIN_ROUTE = 'http://127.0.0.1:8080/'

def index(request):
    return render(request, 'app/index.html')

def appointments_list(request):
    
    json_response = get_json_from_api('appointments')
    appointments_status = json_response['status']
    appointments_content = json_response['content']['results']

    json_response = get_json_from_api('employees')
    employees_status = json_response['status']
    employees_content = json_response['content']['results']

    print(appointments_content)
    print(employees_content)

    context = {}
    if appointments_status == 200 and employees_status == 200:
        context = {'appointments': appointments_content, 'employees': employees_content}

    return render(request, 'app/appointments.html', context)

def get_json_from_api(url_route):
    response = {}
    try:
        response = requests.get(f'{API_MAIN_ROUTE}{url_route}/', headers={'Authorization': f'token {API_TOKEN}'})
    except Exception as e:
        raise e

    if response == {}:
        output = {'status': 404, 'content': {}}
    else:    
        response_code = response.status_code
        response_content = response.content.decode('utf-8')  # first convert the data from bytes to text
        response_content = json.loads(response_content)  # then convert the text to json
        output = {'status': response_code, 'content': response_content}
    return output
