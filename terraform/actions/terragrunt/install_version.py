import subprocess, sys, json
import cdx

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    ret = json.load(file)

print(ret['metadata']['name'])

version = ret['metadata']['name']
try:
    subprocess.run(["tenv", "tg", "install", version], check=True)
    print(f"Installed Terragrunt version: '{version}'")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    exit(1)
