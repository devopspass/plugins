import subprocess, sys, json
import cdx

def remove_helm_release(release_name):
    try:
        subprocess.run(['helm', 'uninstall', release_name], check=True)
        print(f"Removed release: '{release_name}'")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    ret = json.load(file)
    default_env_name = ret['metadata']['name']

remove_helm_release(default_env_name)
