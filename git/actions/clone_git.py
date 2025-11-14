import configparser
import os
from pathlib import Path
import subprocess
import json, sys
from urllib.parse import urlparse

import cdx
import sys

doc = {}

if len(sys.argv) == 2:
    url = sys.argv[1]
else:
    fname_doc = sys.argv[1]
    fname_settings = sys.argv[2]
    with open(fname_doc, 'r') as file:
        doc = json.load(file)
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
git_repo_doc_type = doc.get('metadata', {}).get('doc_type')
if git_repo_doc_type in ['gitlab_repos']:
    clone_source = cdx.settings.get('gitlab.clone_source')

clone_url = None
if clone_source == 'https':
    clone_url = url
elif clone_source == 'ssh':
    clone_url = f"git@{domain}:{path}.git"
else:
    raise ValueError(f'Invalid clone source setting, must be "ssh" or "https", got: {clone_source}')

repo_path = f"{workspace_folder}/{domain}/{path}"

if not os.path.exists(repo_path):
    # Directory does not exist, perform git clone
    try:
        os.makedirs(repo_path, exist_ok=True)
        subprocess.run(['git', 'clone', clone_url, repo_path], check=True)
        print(f"Cloned repository '{url}' ({clone_url}) into '{repo_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
