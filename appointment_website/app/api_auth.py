from json import load as json_load


def get_api_token():
    with open('secrets.json', 'r') as f:
        data = json_load(f)
        return data['api_token']
