import concurrent.futures
import time
import traceback
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

def org_list():
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
                if domain == 'github.com':
                    org['icon'] = org['avatar_url']
                else:
                    org['icon'] = 'assets/icons/apps/github.png'
                for key in r.keys():
                    if key not in ['name', 'url', 'description']:
                        del org[key]
                res.append(org)
            if resp.headers.get('link') and resp.links.get('next', {}).get('url'):
                url = resp.links['next']['url']
            else:
                return res
        elif resp.status_code == 401:
            raise Exception("User not authorized, have you set correct GitHub token in settings?")
        else:
            raise Exception(f"Something went wrong: {resp.content}")

def get_repos(org):
    headers = {
        'Authorization': f"Bearer {token}",
    }
    res = []

    url = f"https://api.{domain}/orgs/{org['name']}/repos"
    while True:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            res = res + resp.json()
        elif resp.status_code == 401:
            raise("User not authorized, have you set correct GitHub token in settings?")
        else:
            time.sleep(2)
        if resp.headers.get('link') and resp.links.get('next', {}).get('url'):
            url = resp.links['next']['url']
        else:
            return res


def list():
    if not domain or domain == '':
        return error("GitHub domain doesnt set in Settings, please set it")
    if not token or token == '':
        return error("GitHub personal token doesnt set in Settings, please set it in GitHub -> Profile -> Developer settings -> Personal tokens")

    try:
        res = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            repos = executor.map(get_repos, org_list())
            # Wait for all tasks to complete
            executor.shutdown(wait=True, cancel_futures=False)
        _res = []
        for rep in repos:
            _res = _res + rep
        for r in _res:
            ___r = r.copy()
            ___r['name'] = ___r['full_name']
            ___r['url'] = f"https://{domain}/{r['full_name']}"
            if domain == 'github.com':
                ___r['icon'] = ___r['avatar_url']
            else:
                ___r['icon'] = 'assets/icons/apps/github.png'

            for key in r.keys():
                if key not in ['name', 'url', 'description', 'icon']:
                    del ___r[key]
            res.append(___r)
    except Exception as e:
        return error("Something went wrong: " + traceback.format_exc())

    return res
