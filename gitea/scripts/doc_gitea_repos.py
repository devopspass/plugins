import concurrent.futures
import time
import traceback
import requests
import cdx

domain = cdx.settings.get('gitea.domain')
token = cdx.settings.get('gitea.token')

def error(msg: str):
    return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': '```' + msg + '```'
            }
        ]

def org_list():
    url = f'{domain}/api/v1/repos/search?limit=999'

    headers = {
        'Authorization': f"Bearer {token}",
    }

    res = []
    while True:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            for r in resp.json().get('data', []):
                res.append({
                    "name": r.get('full_name'),
                    "description": r.get('description'),
                    "url": r.get('html_url'),
                    "parent": r.get('parent'),
                })
            return res
        elif resp.status_code == 401:
            raise Exception("User not authorized, have you set correct GitHub token in settings?")
        else:
            raise Exception(f"Something went wrong: {resp.content}")

def list():
    if not domain or domain == '':
        return error("GitHub domain doesnt set in Settings, please set it")
    if not token or token == '':
        return error("GitHub personal token doesnt set in Settings, please set it in GitHub -> Profile -> Developer settings -> Personal tokens")

    return org_list()
