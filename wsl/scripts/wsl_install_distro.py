import subprocess, sys, json
import cdx

def install_wsl_distro(distro_name):
    cmd = ['wsl', '--install', '-d', distro_name]
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Installed distro '{distro_name}'")

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

install_wsl_distro(doc['metadata']['name'])
