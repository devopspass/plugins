import configparser
import os
from pathlib import Path
import subprocess
import json, sys
from urllib.parse import urlparse

import cdx
import sys

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

opts = cdx.helpers.get_action_options(doc, 'git_clone_repo')

url = doc['metadata']['url']
workspace_folder = cdx.settings.get('user.workspace_folder')

parsed_url = urlparse(url)

# Check if the URL has the correct scheme
if parsed_url.scheme != 'https':
    raise ValueError('Invalid HTTPS URL')

# Extract the domain and path
domain = parsed_url.netloc
path = parsed_url.path.strip('/')

# Construct the SSH URL
ssh_url = f"git@{domain}:{path}.git"

repo_path = f"{workspace_folder}/{domain}/{path}"

if not os.path.exists(repo_path):
    # Directory does not exist, perform git clone
    try:
        os.makedirs(repo_path, exist_ok=True)
        subprocess.run(['git', 'clone', ssh_url, repo_path], check=True)
        print(f"Cloned repository '{url}' ({ssh_url}) into '{repo_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
