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

def get_pages(base_url, bearer_token, space, user=None):
    is_cloud = 'atlassian.net' in base_url

    # Define the initial API endpoint
    auth = None
    if is_cloud:
        auth = (user, bearer_token)

    url = f"{base_url}/rest/api/content?spaceKey={space}&limit=100&expand=title,space"
    print(url)
    # Define the headers
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    pages = []

    while url and url != base_url:
        # Make the GET request to the API
        response = requests.get(url, headers=headers, auth=auth)

        # Check if the request was successful
        if response.status_code != 200:
            return error(f"Failed to retrieve pages: {url} {response.status_code} {response.text}")

        # Parse the JSON response
        data = response.json()

        # Extract page titles and URLs
        for page in data.get('results', []):
            name = page.get('title', '')
            page_url = f"{base_url}{page.get('_links', {}).get('webui', '')}"
            key = page.get('space', {}).get('key')
            pages.append({
                'name': name,
                'url': page_url,
                'space': f"[{key}]({base_url}/display/{key})"
            })

        # Get the next URL for pagination
        url = base_url + data.get('_links', {}).get('next', '')

    return pages

def list_docs():
    base_url = cdx.settings.get('confluence.server')
    bearer_token = cdx.settings.get('confluence.token')
    user = cdx.settings.get('confluence.user')


    if not base_url or not bearer_token:
        return error("Please specify Confluence server URL and token in Settings.")

    if not cdx.settings.get('confluence.spaces'):
        return error("Please specify comma separated list of spaces to fetch pages from in Settings.")

    is_cloud = 'atlassian.net' in base_url
    base_url = base_url.rstrip('/')
    if is_cloud and not '/wiki' in base_url:
        base_url = base_url.rstrip('/') + '/wiki'

    spaces = cdx.settings.get('confluence.spaces').split(',')

    pages = []
    for space in spaces:
        pages += get_pages(base_url, bearer_token, space, user)

    return pages
