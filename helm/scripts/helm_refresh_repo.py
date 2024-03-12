import subprocess, sys, json, os
import cdx

action = 'helm_refresh_repo'

def refresh_helm_repo(repo_name):
    try:
        ret = subprocess.run(['helm', 'repo', 'update', repo_name], check=True, capture_output=True)
        print(f"Repo refreshed environment: '{repo_name}':\n {ret.stdout.decode('utf-8')}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

repo_name = doc['metadata']['name']
refresh_helm_repo(repo_name)
