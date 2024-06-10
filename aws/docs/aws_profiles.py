import configparser
from pathlib import Path
import subprocess
import re, json, os
import cdx
import botocore.session

def list():
    aws = []

    session = botocore.session.get_session()
    profiles = session.available_profiles

    config = configparser.RawConfigParser()
    path = os.path.expanduser('~/.aws/credentials')

    aws_info_file = os.path.join(cdx.helpers.dop_home_path(), 'tmp', 'aws_accounts.json')
    if os.path.exists(aws_info_file):
        with open(aws_info_file, 'r') as file:
                aws_info = json.load(file)
    else:
        aws_info = {}

    if not os.path.exists(path):
        Path(path).touch()

    config.read(path)

    key_id = ''
    if config.has_section('default'):
      key_id = config.get('default', 'aws_session_token')

    for p in profiles:
        if config.has_section(p):
            active = (key_id == config.get(p, 'aws_session_token') and key_id != '' and key_id != 'xxx')
            if p == 'default':
                continue
            aws.append(
                {
                    'name': p,
                    'active': active,
                    'account_id': aws_info.get(p, {}).get('account_id', "0"),
                    'profile_id': aws_info.get(p, {}).get('profile_id', "0"),
                    'description': aws_info.get(p, {}).get('description', "0"),
                    'email': aws_info.get(p, {}).get('email', ""),
                }
            )

    aws = sorted(aws, key=lambda p: p['name'])
    return aws
