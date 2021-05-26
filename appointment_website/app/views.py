import requests
import json
from django.shortcuts import render

from . import api_auth

API_TOKEN = api_auth.get_api_token()

def index(request):
    
    response = requests.get('http://127.0.0.1:8080/appointments/', headers={'Authorization': f'token {API_TOKEN}'})

    response_code = response.status_code
    response_content = response.content.decode('utf-8')

    appointments = json.loads(response_content)

    output = {}
    if response_code == 200 and 'results' in appointments.keys() and len(appointments['results']) > 0:
        output = appointments

    return render(request, 'app/index.html', output)