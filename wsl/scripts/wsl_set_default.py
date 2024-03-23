import subprocess, sys, json
import cdx

def wsl_set_default(distro_name):
    cmd = ['wsl', '--set-default', distro_name]
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Default distro '{distro_name}'")

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

wsl_set_default(doc['metadata']['name'])
