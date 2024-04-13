action = "k3s_install"

import os
import json, sys, time
import webbrowser
import subprocess

import requests
import cdx

from pathlib import Path


fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

opts = cdx.helpers.get_action_options(doc, action)
name = doc.get('metadata', {}).get('name')

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


if name:
    token = doc['metadata']['opts']['aws_sso_token']
    # accounts = doc['metadata']['opts']['end_result']

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
        accounts = response.json()['result']
        acnt = {}
        accounts_to_check = []
        for ac in accounts:
            if ac['searchMetadata']['AccountName'] in name:
                accounts_to_check.append(ac)
        for ac in accounts_to_check:
            account_name = ac['searchMetadata']['AccountName']
            account_id = ac['searchMetadata']['AccountId']
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
            roles = requests.get(url, headers=headers).json()['result']
            for role in roles:
                role_name = role['name']
                if f"{account_name}-{role_name}" == name:
                    url = f"https://portal.sso.us-east-1.amazonaws.com/federation/credentials?account_id={account_id}&role_name={role_name}"
                    # {
                    #     'roleCredentials': {
                    #         'accessKeyId': 'XXXXXXX',
                    #         'secretAccessKey': '+XXXXXXX+XXXXXX+XXXXx/xx',
                    #         'sessionToken': 'XXX+XX/XXX+XXX/XXX',
                    #         'expiration': 123456
                    #     }
                    # }
                    creds = requests.get(url, headers=headers).json()['roleCredentials']
                    set_aws_credentials(name, creds['accessKeyId'], creds['secretAccessKey'], creds['sessionToken'])
                    print(f"Credentials for AWS profile '{name}' were successfully updated.")
    else:
        print("Error:", response.text)
        exit(1)

# curl '' \
#   -H 'accept: application/json, text/plain, */*' \
# cmd = settings['docker.command']

