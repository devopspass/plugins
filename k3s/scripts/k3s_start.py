action = "k3s_install"

import json, sys, time
import webbrowser
import subprocess
import cdx


fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

opts = cdx.helpers.get_action_options(doc, action)
version = opts.get('version', {}).get('value')

cmd = settings['docker.command']
port = settings['autok3s.port']

_c = f" run -itd --restart=unless-stopped --name autok3s -p {port}:8080 "

# Network
if cdx.helpers.is_macos() or cdx.helpers.is_windows():
    _c += f" -e DOCKER_HOST=\"\" "
else:
    _c += f' --network host '
_c += " --volume /var/run/docker.sock:/var/run/docker.sock "

# Image
_c += f" cnrancher/autok3s:v{version} "

cmd = cmd.replace('%DOCKER_COMMAND%', _c)
print(cmd)

output = subprocess.run(cmd, text=True, capture_output=True, check=True, shell=True)

if output.returncode == 0:
    print(output.stdout)
    print(output.stderr)
    print("Opening K3s endpoint...")
    time.sleep(3)
    webbrowser.open_new_tab(f'http://127.0.0.1:{port}/')
else:
    print("Something went wrong...")
    print(output.stdout)
    print(output.stderr)
    exit(1)
