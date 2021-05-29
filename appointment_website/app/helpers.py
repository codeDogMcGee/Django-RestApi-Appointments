import requests
import json

from . import api_auth

API_TOKEN = api_auth.get_api_token()
API_MAIN_ROUTE = 'http://127.0.0.1:8080/'


def get_json_from_api(url_endpoint):
    response = {}
    try:
        if len(url_endpoint) > 0:
            url_endpoint = url_endpoint + '/' if url_endpoint[-1] != '/' else url_endpoint
            request_url = f'{API_MAIN_ROUTE}{url_endpoint}'
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