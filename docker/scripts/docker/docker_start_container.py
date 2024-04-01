import docker
import time, json, sys, os
import cdx

action = 'docker_start_container'
fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

opts = cdx.helpers.get_action_options(doc, action)
name = opts.get('name', {}).get('value')
image = opts.get('image', {}).get('value')
command = opts.get('command', {}).get('value')
volumes = opts.get('volumes', {}).get('value').strip().split(',')
ports = opts.get('ports', {}).get('value')
network = opts.get('network', {}).get('value')
network_container = opts.get('network_container', {}).get('value')
start_as = opts.get('start_as', {}).get('value').split('|')[-1]

cmd = settings['docker.command']
_c = f" run --rm "
# Container name
if name != '':
    _c += f"--name {name} "

# Network
_c += f"--network {network} "

# Start as
_c += f"{start_as} "

# Volumes
for vol in volumes:
    if vol != '':
        _c += f"--volume {vol} "

# Image
_c += f"{image} "

# Command
if command != '':
    _c += f"{command}"

cmd = cmd.replace('%DOCKER_COMMAND%', _c)
print(cmd)
os.system(cmd)
