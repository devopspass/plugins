import json, sys, subprocess
import cdx

action = 'helm_add_repo'
fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

opts = cdx.helpers.get_action_options(doc, action)
name = opts.get('repo_name', {}).get('value')
url = opts.get('repo_url', {}).get('value')

def add_helm_repo(name, url):
    try:
        # Run "conda env create" using the generated YAML file
        subprocess.run(['helm', 'repo', 'add', name, url], check=True)
        print(f"Helm repo '{name}' ({url}) added successfully.")
        exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Error adding Helm repo: {e}")
        exit(1)

add_helm_repo(name, url)

