
action = "k3s_install"

import os
from random import randrange
import json, sys, time
import requests
import cdx
import concurrent.futures
import requests
from pathlib import Path


fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

name = doc.get('metadata', {}).get('name')
pull_credentials = True

# If script running for document, pull creds, if for app, depends on option
opts = cdx.helpers.get_action_options(doc, 'aws_refresh_sso_tokens')
if opts:
    pull_credentials = opts.get('refresh_creds', {}).get('value') == 'true'

import configparser

# Drop SSO config options if we have creds
def delete_sso_config(name: str):
    profile_name = f"profile {name}"
    config = configparser.RawConfigParser()
    path = os.path.expanduser('~/.aws/config')
    if not os.path.exists(path):
        Path(path).touch()
    config.read(path)
    if not config.has_section(profile_name):
        config.add_section(profile_name)

    config.remove_option(profile_name, 'sso_start_url')
    config.remove_option(profile_name, 'sso_region')
    config.remove_option(profile_name, 'sso_account_id')
    config.remove_option(profile_name, 'sso_role_name')
    with open(path, 'w') as configfile:
      config.write(configfile)

# [default]
# aws_access_key_id=ASIAIOSFODNN7EXAMPLE
# aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# aws_session_token = IQoJb3JpZ2luX2IQoJb3JpZ2luX2IQoJb3JpZ2luX2IQoJb3JpZ2luX2IQoJb3JpZVERYLONGSTRINGEXAMPLE
def set_aws_credentials(profile_name: str, access_key: str, secret_key: str, session_token: str):
    config = configparser.RawConfigParser()
    path = os.path.expanduser('~/.aws/credentials')
    if not os.path.exists(path):
        Path(path).touch()
    config.read(path)
    if not config.has_section(profile_name):
        config.add_section(profile_name)
    config.set(profile_name, 'aws_access_key_id', access_key)
    config.set(profile_name, 'aws_secret_access_key', secret_key)
    config.set(profile_name, 'aws_session_token', session_token)
    with open(path, 'w') as configfile:
      config.write(configfile)
    delete_sso_config(profile_name)

def add_profile(name: str):
    profile_name = f"profile {name}"
    config = configparser.RawConfigParser()
    path = os.path.expanduser('~/.aws/config')
    if not os.path.exists(path):
        Path(path).touch()
    config.read(path)
    if not config.has_section(profile_name):
        config.add_section(profile_name)

    with open(path, 'w') as configfile:
      config.write(configfile)

def get_profiles(ac):
    retries = 20

    while True:
        url = f"https://portal.sso.us-east-1.amazonaws.com/instance/appinstance/{ac['id']}/profiles"
        # {
        #     "paginationToken": null,
        #     "result": [
        #         {
        #             "id": "p-XXXXXX",
        #             "name": "PROFILE_NAME",
        #             "description": "",
        #             "url": "https://portal.sso.us-east-1.amazonaws.com/saml/assertion/idp/XXXXXXXX==",
        #             "protocol": "SAML",
        #             "relayState": null
        #         },
        #         ...
        #     ]
        # }
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
          return {
              'account': ac['searchMetadata']['AccountName'],
              'account_id': ac['searchMetadata']['AccountId'],
              'profiles': resp.json()['result']
            }
        else:
            time.sleep(randrange(10))
        retries = retries - 1
        if retries == 0:
            return {}

def get_credentials(role):
    account_name = role['account']
    account_id = role['account_id']
    res = []

    for profile in role['profiles']:
        role_name = profile['name']
        profile_name = f"{account_name}-{role_name}"

        retries = 20
        while True:
            if profile_name == name or pull_credentials:
                url = f"https://portal.sso.us-east-1.amazonaws.com/federation/credentials?account_id={account_id}&role_name={role_name}"
                # {
                #     'roleCredentials': {
                #         'accessKeyId': 'XXXXXXX',
                #         'secretAccessKey': '+XXXXXXX+XXXXXX+XXXXx/xx',
                #         'sessionToken': 'XXX+XX/XXX+XXX/XXX',
                #         'expiration': 123456
                #     }
                # }
                creds = requests.get(url, headers=headers)
                if creds.status_code == 200:
                    res.append({'profile': profile_name, 'creds': creds.json()['roleCredentials']})
                    break
                else:
                    time.sleep(2)

            retries = retries - 1
            if retries == 0:
                print(f"Failed to refresh creds for '{profile_name}' by timeout")
                break

    return res


### Main
path = os.path.expanduser('~/.aws/')
if not os.path.exists(path):
    Path(path).mkdir()

token = doc['metadata']['opts']['aws_sso_token']

## Get Accounts in parralell
url = f'https://portal.sso.us-east-1.amazonaws.com/instance/appinstances'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'x-amz-sso-bearer-token': token,
    'x-amz-sso_bearer_token': token,
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # {
    #     'id': 'ins-XXXXX',
    #     'name': 'XXXXXx (YYYY-YYYY)',
    #     'description': 'AWS administrative console',
    #     'applicationId': 'app-YYYYYYY',
    #     'applicationName': 'AWS Account',
    #     'icon': 'https://static.global.sso.amazonaws.com/app-YYYYYYY/icons/default.png',
    #     'searchMetadata': {
    #         'AccountId': '123456',
    #         'AccountName': 'ZZZ-ZZZ',
    #         'AccountEmail': 'e@mail.com'
    #     }
    # }
    batch_size = 20
    accounts = response.json()['result']
    acnt = {}
    accounts_to_check = []
    if doc['metadata']['doc_type'] == 'application':
        accounts_to_check = accounts
    else:
        for ac in accounts:
            if ac['searchMetadata']['AccountName'] in name:
                accounts_to_check.append(ac)

    #### Get Profiles in parralell
    print(f"Total accounts: {len(accounts)}")

    # Process each batch in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
        roles = executor.map(get_profiles, accounts_to_check)
        # Wait for all tasks to complete
        executor.shutdown(wait=True, cancel_futures=False)
        creds_list = []

        for role in roles:
            # print(role)
            if not role.get('profiles'):
                continue
            creds_list.append(role)
            for profile in role['profiles']:
                nm = role['account'] + "-" + profile['name']
                print(f"Adding profile '{nm}'")
                add_profile(nm)

        #### Get Credentials in parralell
        print(f"Total profiles found: {len(creds_list)}. Pulling credentials")

        if pull_credentials:
            # Process each batch in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
                results = executor.map(get_credentials, creds_list)
                # Wait for all tasks to complete
                executor.shutdown(wait=True, cancel_futures=False)

                for _res in results:
                    for res in _res:
                        profile_name = res['profile']
                        creds = res['creds']
                        set_aws_credentials(profile_name, creds['accessKeyId'], creds['secretAccessKey'], creds['sessionToken'])
                        print( f"Credentials for AWS profile '{profile_name}' were successfully updated.")

else:
    print("Error: ", response.text)
    exit(1)
