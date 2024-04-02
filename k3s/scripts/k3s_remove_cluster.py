import requests, cdx, json, sys

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

port = settings.get('autok3s.port', '8080')
id = doc['metadata']['id']

url = f"http://127.0.0.1:{port}/v1/clusters/{id}"
# Send GET request to fetch clusters data
response = requests.delete(url)

# Check if request was successful
if response.status_code == 200:
    print(f"K3s cluster '{id}' was removed")
    exit(0)
else:
    # Return error dictionary
    print(f"Can't remove k3s cluster '{id}' - ({response.status_code}): {response.content}")
    exit(1)