import subprocess, sys, json
import cdx

def remove_node_version(node_version):
    try:
        subprocess.run(['bash', '-c', f"source ~/.nvm/nvm.sh && nvm uninstall {node_version}"], check=True)
        print(f"Removed node version: '{node_version}'")
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

remove_node_version(node_version)
