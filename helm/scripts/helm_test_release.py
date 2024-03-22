import subprocess, sys, json
import cdx

def test_helm_release(release_name):
    res = subprocess.run(['helm', 'test', release_name], capture_output=True)
    print(f"Tested release: '{release_name}'")
    print(res.stderr.decode('utf-8'))
    print(res.stdout.decode('utf-8'))

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    ret = json.load(file)
    default_env_name = ret['metadata']['name']

test_helm_release(default_env_name)
