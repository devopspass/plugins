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
    if not os.path.exists(path):
        Path(path).touch()

    config.read(path)

    key_id = ''
    if config.has_section('default'):
      key_id = config.get('default', 'aws_access_key_id')

    for p in profiles:
        active = key_id == config.get(p, 'aws_access_key_id')
        if p == 'default':
            continue
        aws.append(
            {
                'name': p,
                'active': active
            }
        )

    aws = sorted(aws, key=lambda p: p['name'])
    return aws
