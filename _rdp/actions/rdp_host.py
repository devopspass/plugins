import os
import json
import sys

settings = {}
doc = {}

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]
with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)


ip = doc['metadata']['ip']
cmd = settings['rdp.command']
if settings.get('actions.rdp_host'):
    user = settings.get('actions.rdp_host', {}).get(f"{ip}_rdp_user", 'Administrator')
    jh = settings.get('actions.rdp_host', {}).get(f"{ip}_rdp_jumphost")
    port = settings.get('actions.rdp_host', {}).get(f"{ip}_rdp_port", '3389')
    command = settings.get('actions.rdp_host', {}).get(f"{ip}_rdp_command", '')
else:
    user = 'Administrator'
    port = '3389'
    command = ''
    jh = ''

# terminator -e 'ssh -p %PORT% %JUMPHOST_OPTIONS% %USER%@%SERVER_IP%'
cmd = cmd.replace('%PORT%', port)
cmd = cmd.replace('%USER%', user)
cmd = cmd.replace('%SERVER_IP%', ip)
cmd = cmd.replace('%COMMAND%', command)
cmd = cmd.replace('%JUMPHOST_OPTIONS%', '')

ret = os.system(cmd)
print(f"RDP: '{cmd}' exit code: {ret}")
if ret != 0:
    sys.exit(1)