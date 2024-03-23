import subprocess, sys, json
import cdx

def wsl_terminal(distro_name):
    cmd = ['cmd.exe', '/c', f'wsl -d {distro_name}']
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Terminal for distro '{distro_name}'")

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

wsl_terminal(doc['metadata']['name'])
