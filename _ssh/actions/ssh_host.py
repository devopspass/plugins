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
cmd = settings['ssh.command']
if settings.get('actions.ssh_host'):
    user = settings.get('actions.ssh_host', {}).get(f"{ip}_ssh_user", 'root')
    jh = settings.get('actions.ssh_host', {}).get(f"{ip}_ssh_jumphost")
    port = settings.get('actions.ssh_host', {}).get(f"{ip}_ssh_port", '22')
    command = settings.get('actions.ssh_host', {}).get(f"{ip}_ssh_command", '')
else:
    user = 'root'
    port = '22'
    command = ''
    jh = ''
jh_opts = settings.get('ssh.command.jumphost_options', '')

if not jh or jh == '':
    jh_opts = ''
else:
    jh_opts = jh_opts.replace('%JUMPHOST%', jh)
# terminator -e 'ssh -p %PORT% %JUMPHOST_OPTIONS% %USER%@%SERVER_IP%'
cmd = cmd.replace('%PORT%', port)
cmd = cmd.replace('%USER%', user)
cmd = cmd.replace('%SERVER_IP%', ip)
cmd = cmd.replace('%COMMAND%', command)
cmd = cmd.replace('%JUMPHOST_OPTIONS%', jh_opts)

ret = os.system(cmd)
print(f"SSH: '{cmd}' exit code: {ret}")
if ret != 0:
    sys.exit(1)