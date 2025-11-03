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

import requests

def list_docs():
    base_url = cdx.settings.get('confluence.server')
    bearer_token = cdx.settings.get('confluence.token')
    user = cdx.settings.get('confluence.user')

    is_cloud = 'atlassian.net' in base_url if base_url else False

    if not base_url or not bearer_token:
        return error("Please specify Confluence server URL and token in Settings.")

    if is_cloud and not user:
        return error("Please specify Confluence user email for Atlassian Cloud in Settings.")
    
    base_url = base_url.rstrip('/')

    if 'wiki' in base_url:
        base_url = base_url.replace('/wiki', '')
    # Define the API endpoint
    if is_cloud:
        url = f"{base_url}/wiki/api/v2/spaces?limit=250"
    else:
        url = f"{base_url}/api/v2/spaces?limit=250"

    auth = None
    if is_cloud:
        auth = (user, bearer_token)
    # Define the headers
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    # Make the GET request to the API
    response = requests.get(url, headers=headers, auth=auth)

    # Check if the request was successful
    if response.status_code != 200:
        return error(f"Failed to retrieve workspaces: {response.status_code} {response.text}")

    print(url)
    # Parse the JSON response
    data = response.json()

    # Extract workspace names and descriptions
    workspaces = []
    for space in data.get('results', []):
        name = space.get('name', 'No name')
        if space.get('description'):
            description = space.get('description', {}).get('plain', {}).get('value', '')
        else:
            description = ''
        workspaces.append({
            'name': name,
            'key': space.get('key'),
            'url': base_url + '/display/' + space.get('key'),
            'description': description,
            }
        )

    return workspaces
