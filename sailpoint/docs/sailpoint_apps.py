import subprocess
import json
import yaml
import requests
import cdx

def error(msg: str):
    return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': '```' + msg + '```'
            }
        ]

def get_sailpoint_token(tenant, client_id, client_secret):
    """
    Fetches an OAuth token from the SailPoint API.

    :param tenant: The tenant for the SailPoint instance.
    :param client_id: The client ID for OAuth authentication.
    :param client_secret: The client secret for OAuth authentication.
    :return: The access token as a string.
    """
    url = f'https://{tenant}.api.identitynow.com/oauth/token'
    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while obtaining the token: {e}")
        return None

def list():
    tenant = cdx.settings.get('sailpoint.tenant')
    client_id = cdx.settings.get('sailpoint.client_id')
    client_secret = cdx.settings.get('sailpoint.client_secret')

    token = get_sailpoint_token('epicgames', client_id, client_secret)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # endpoint = f'{base_url}/identitynow/v3/requests'
    endpoint = f"https://{tenant}.api.identitynow.com/v2/identity/apps/?offset=0&limit=2500&count=true&excludeLauncherOnlyApps=true&excludeAccessProfiles=true"
    ret = []
    reqs = []
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            response.raise_for_status()
            reqs = response.json()
        else:
            return error(f"Failed to get applications: ({response.status_code}) - {str(response.content)}")
    except requests.exceptions.RequestException as e:
        return error(f"An error occurred: {e}")

    ret = []
    for req in reqs:
        ret.append({
            'name': req.get('name'),
            # 'icon': f"https://{tenant}.api.identitynow.com/ums/icons-public/application/{req.get('appRoleId')}",
            'url': f"https://{tenant}.identitynow.com/ui/d/request-center/request-access",
            'description': req.get('description'),
        })
    return ret
