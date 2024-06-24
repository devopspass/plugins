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

def list():
    base_url = cdx.settings.get('confluence.server')
    base_url = base_url.rstrip('/')
    bearer_token = cdx.settings.get('confluence.token')

    # Define the API endpoint
    url = f"{base_url}/rest/api/space?type=global&limit=9999&expand=name,key,description"

    # Define the headers
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    # Make the GET request to the API
    response = requests.get(url, headers=headers)

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
        description = space.get('description', {}).get('plain', {}).get('value', '')
        workspaces.append({
            'name': name,
            'key': space.get('key'),
            'url': base_url + '/display/' + space.get('key'),
            'description': description,
            }
        )

    return workspaces
