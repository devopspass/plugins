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

name = doc['metadata']['name']

cmd = settings['docker.command']
_c = f" attach {name} "

cmd = cmd.replace('%DOCKER_COMMAND%', _c)
print(cmd)
os.system(cmd)
