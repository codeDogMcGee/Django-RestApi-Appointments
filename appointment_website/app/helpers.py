import requests
import json

from . import api_auth
from .models import CustomUser

API_TOKEN = api_auth.get_api_token()
API_MAIN_ROUTE = 'http://127.0.0.1:8080/'

APPOINTMENT_LENGTH_MINTUES = 30


def get_json_from_api(url_endpoint: str) -> dict[str, object]:
    response = {}
    try:
        if len(url_endpoint) > 0:
            request_url = _create_request_url(url_endpoint)
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


def post_json_to_api(url_endpoint: str, json_object: object) -> dict[str, object]:
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


def format_phone_number(phone_number: str) -> str:
    if len(phone_number) == 10:
        try:
            int(phone_number) # make sure it's all numbers
            return f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
        except:
            pass
    return phone_number


def _create_request_url(endpoint: str) -> str:
    endpoint = endpoint + '/' if endpoint[-1] != '/' else endpoint
    return f'{API_MAIN_ROUTE}{endpoint}'


def get_groups_for_user(user: CustomUser) -> list[str]:
    groups = []
    if user in CustomUser.objects.filter(group__name='Customers'): # if user in Customers group
        groups.append('Customers')
    elif user in CustomUser.objects.filter(group__name='Employees'): # if user in Employees group
        groups.append('Employees')
    return groups