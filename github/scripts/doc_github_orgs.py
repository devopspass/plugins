import subprocess
import re, json

import requests
import cdx

domain = cdx.settings.get('github.domain')
token = cdx.settings.get('github.token')

def error(msg: str):
    return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': '```' + msg + '```'
            }
        ]

def list():
    if not domain or domain == '':
        return error("GitHub domain doesnt set in Settings, please set it")
    if not token or token == '':
        return error("GitHub personal token doesnt set in Settings, please set it in GitHub -> Profile -> Developer settings -> Personal tokens")

    url = f'https://api.{domain}/organizations?per_page=999'

    headers = {
        'Authorization': f"Bearer {token}",
    }

    res = []
    while True:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            for r in resp.json():
                org = r.copy()
                org['name'] = org['login']
                org['url'] = f"https://{domain}/orgs/{org['name']}/repositories"
                # org['icon'] = org['avatar_url']
                for key in r.keys():
                    if key not in ['name', 'url', 'description']:
                        del org[key]
                res.append(org)
            if resp.headers.get('link') and resp.links.get('next', {}).get('url'):
                url = resp.links['next']['url']
            else:
                return res
        else:
            return error(f"Something went wrong: {resp.content}")
