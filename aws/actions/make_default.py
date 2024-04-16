import configparser
import os
from pathlib import Path
import time
import urllib, json, sys
import webbrowser
import requests # 'pip install requests'
import boto3 # AWS SDK for Python (Boto3) 'pip install boto3'
import cdx
import sys

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

opts = cdx.helpers.get_action_options(doc, 'aws_open_console')

profile = doc['metadata']['name']

config = configparser.RawConfigParser()
path = os.path.expanduser('~/.aws/credentials')
if not os.path.exists(path):
    Path(path).touch()

config.read(path)

if not config.has_section(profile):
    print(f"Cant find credentials for profile '{profile}'")
    exit(1)

if not config.has_section('default'):
    config.add_section('default')

for opt in ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']:
    config.set('default', opt, config.get(profile, opt))

with open(path, 'w') as configfile:
    config.write(configfile)
