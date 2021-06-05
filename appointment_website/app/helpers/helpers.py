from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.formats import time_format
import requests
import json

import app.api_auth

API_TOKEN = app.api_auth.get_api_token()
API_MAIN_ROUTE = 'http://127.0.0.1:8080/'

APPOINTMENT_LENGTH_MINTUES = 30

MAIN_DATE_FORMAT = 'm/d/Y'
MAIN_TIME_FORMAT = 'h:i a'

USER_GROUPS = {'employees': 'Emplyoees', 'customers':'Customers'}

VALID_DATE_INPUT_FORMATS = ['%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d']

def get_json_from_api(url_endpoint: str) -> dict[str, object]:
    response = {}
    try:
        if len(url_endpoint) > 0:
            request_url = _create_request_url(url_endpoint)
            # print('\nAPI GET REQUEST', request_url,'\n')
            response = requests.get(request_url, headers={'Authorization': f'token {API_TOKEN}'})
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


def post_or_put_json_to_api(post_or_put: str, url_endpoint: str, json_object: object) -> dict[str, object]:
    post_or_put = post_or_put.upper()
    assert post_or_put in ['POST', 'PUT']
    response = {}
    try:
        if len(url_endpoint) > 0:
            request_url = _create_request_url(url_endpoint)
            print('\nPOST OR PUT REQUEST', request_url,'\n')
            if post_or_put == 'POST':
                response = requests.post(request_url, data=json_object, headers={'Authorization': f'token {API_TOKEN}'})
            else:
                response = requests.put(request_url, data=json_object, headers={'Authorization': f'token {API_TOKEN}'})
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


def put_json_to_api(url_endpoint: str, json_object: object) -> dict[str, object]:
    response = {}
    try:
        if len(url_endpoint) > 0:
            request_url = _create_request_url(url_endpoint)
            response = requests.post(request_url, data=json_object, headers={'Authorization': f'token {API_TOKEN}'})
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


def delete_api_object(url_endpoint: str):
    response = {}
    try:
        request_url = _create_request_url(url_endpoint)
        print('\n\nDELETE REQUEST URL:\n', request_url, '\n\n')
        response = requests.delete(request_url, headers={'Authorization': f'token {API_TOKEN}'})
    except Exception as e:
        raise e
    
    status_code = 404 if response == {} else response.status_code
    return {'status': status_code}



def format_phone_number(phone_number: str) -> str:
    if len(phone_number) == 10:
        try:
            int(phone_number) # make sure it's all numbers
            return f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
        except:
            pass
    return phone_number


def _create_request_url(endpoint: str) -> str:
    endpoint = endpoint + '/' if endpoint[-1] != '/' else endpoint # must have a trailing '/'
    endpoint = endpoint[1:] if endpoint[0] == '/' else endpoint # can't have a leading '/'
    return f'{API_MAIN_ROUTE}{endpoint}'


def initialize_groups() -> dict[str, (object, bool)]: 
    groups = ['Employees', 'Customers', 'Managers']
    output = {}
    for group_name in groups:
        output[group_name] = Group.objects.get_or_create(name=group_name) # return tuple (group_object, created_bool)
    return output


def get_appointment_times():
    start_time = timezone.datetime(2000,1,1,7,0,0)
    end_time = timezone.datetime(2000,1,1,18,30,0)

    output = []
    _time = start_time
    while _time <= end_time:
        output.append((_time.time(), time_format(_time, MAIN_TIME_FORMAT)))
        _time += timezone.timedelta(minutes=APPOINTMENT_LENGTH_MINTUES)
    # return a tuple used by forms.Select (drop-down) in a format of (key, value)
    return output
