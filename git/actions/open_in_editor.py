import json
import subprocess
import sys
from urllib.parse import urlparse
import webbrowser
import os
import cdx

editor_command = cdx.settings.get('editor.command')
workspace_folder = cdx.settings.get('user.workspace_folder')

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]
with open(fname_doc, 'r') as file:
    doc = json.load(file)
url = doc['metadata']['url']

# Run the shell script with the JSON file as an argument
plugin_path = os.path.join(cdx.helpers.plugins_path(), 'git/actions/clone_git.py')
result = subprocess.run(
    [
        cdx.helpers.python_bin_path(),
        '-u',
        plugin_path,
        url
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=True
)

print(result.stderr)
print(result.stdout)

parsed_url = urlparse(url)

# Check if the URL has the correct scheme
if parsed_url.scheme != 'https':
    raise ValueError('Invalid HTTPS URL')

# Extract the domain and path
domain = parsed_url.netloc
path = parsed_url.path.strip('/')

repo_path = f"{workspace_folder}/{domain}/{path}"

editor_command = editor_command.replace('%PATH%', repo_path)


subprocess.run(editor_command, shell=True)
