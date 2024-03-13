import subprocess, sys, json
import cdx

def activate_node_version(node_version):
    try:
        subprocess.run(['bash', '-c', f"unset npm_config_prefix && source ~/.nvm/nvm.sh && nvm alias default {node_version} --no-colors"], check=True)
        print(f"Activated node version: '{node_version}'")
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

node_version = ret['metadata']['name']

activate_node_version(node_version)
