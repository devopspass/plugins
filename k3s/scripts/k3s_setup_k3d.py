import requests, cdx, json, sys
import yaml

action = 'k3s_setup_k3d'
fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

port = settings.get('autok3s.port', '8080')
opts = cdx.helpers.get_action_options(doc, action)
id = yaml.safe_load(opts.get('cluster_name', {}).get('value'))

def create_cluster():
    url = f'http://127.0.0.1:{port}/v1/clusters'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "datastore-cafile-content": "",
        "datastore-certfile-content": "",
        "datastore-keyfile-content": "",
        "master": "1",
        "master-extra-args": "",
        "masters-memory": "",
        "name": id,
        "network": "",
        "registry": "",
        "registry-content": "",
        "token": "",
        "worker": "1",
        "worker-extra-args": "",
        "workers-memory": "",
        "provider": "k3d",
        "options": {
            "api-port": "0.0.0.0:0",
            "envs": None,
            "gpus": "",
            "image": "docker.io/rancher/k3s:v1.28.5-k3s1",
            "labels": None,
            "masters-memory": "",
            "no-image-volume": False,
            "no-lb": False,
            "ports": None,
            "volumes": None,
            "workers-memory": ""
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return response.json()
    else:
        # Handle error responses here
        print("Error:", response.text)
        return None

# Example usage:
response_json = create_cluster()
print(response_json)

# Check if request was successful
if response_json:
    print(f"K3s cluster '{id}' was created")
    exit(0)
else:
    # Return error dictionary
    print(f"Can't create k3s cluster '{id}'")
    exit(1)