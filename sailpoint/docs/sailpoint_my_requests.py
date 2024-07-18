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

def get_sailpoint_user_requests(tenant, client_id, client_secret):
    """
    Fetches the current user requests from SailPoint.

    :param base_url: The base URL for the SailPoint API (e.g., 'https://your-sailpoint-instance.com').
    :param token: The token for authentication.
    :return: A list of dictionaries containing user requests.
    """
    base_url = f'https://{tenant}.identitynow.com/'

    token = get_sailpoint_token('epicgames', client_id, client_secret)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # endpoint = f'{base_url}/identitynow/v3/requests'
    endpoint = f"https://{tenant}.api.identitynow.com/beta/access-request-status?regarding-identity=me&limit=50&offset=0&count=true&sorters=-created"

    try:
        response = requests.get(endpoint, headers=headers)
        # print(response.content)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def list():
    tenant = cdx.settings.get('sailpoint.tenant')
    client_id = cdx.settings.get('sailpoint.client_id')
    client_secret = cdx.settings.get('sailpoint.client_secret')

    reqs = get_sailpoint_user_requests(tenant, client_id, client_secret)
    ret = []
    for req in reqs:
        icon = 'assets/icons/general/ok.png'
        if req.get('state') == 'REJECTED':
            icon = 'assets/icons/general/error.png'
        if req.get('state') == 'EXECUTING':
            icon = 'assets/icons/general/link.png'
        ret.append({
            'name': req.get('name'),
            'icon': icon,
            'url': f'https://{tenant}.identitynow.com/ui/d/request-center/my-requests#{req.get("accessRequestId")}',
            'description': req.get('description'),
            'state': req.get('state'),
            'id': req.get('accessRequestId'),
            'error': req.get('errorMessages')
        })
    return ret
