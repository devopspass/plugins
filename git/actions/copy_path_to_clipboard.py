from pandas.io import clipboard
from urllib.parse import urlparse
import sys, cdx
import json

fname_doc = sys.argv[1]
doc = {}

with open(fname_doc, 'r') as file:
    doc = json.load(file)

workspace_folder = cdx.settings.get('user.workspace_folder')
url = doc['metadata']['url']

parsed_url = urlparse(url)

# Check if the URL has the correct scheme
if parsed_url.scheme != 'https':
    raise ValueError('Invalid HTTPS URL')

# Extract the domain and path
domain = parsed_url.netloc
path = parsed_url.path.strip('/')
workspace_folder = workspace_folder.rstrip('/')

repo_path = f"{workspace_folder}/{domain}/{path}"

clipboard.copy(repo_path)
print(f"Copied to clipboard '{repo_path}'")
exit(0)
