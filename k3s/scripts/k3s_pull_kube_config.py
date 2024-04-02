import requests, cdx, json, sys

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

port = settings.get('autok3s.port', '8080')
id = doc['metadata']['id']

def download_kubeconfig(cluster_id):
    url = f'http://127.0.0.1:{port}/v1/clusters/{cluster_id}?action=download-kubeconfig'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {'id': cluster_id}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle error responses here
        print("Error:", response.text)
        return None

config = download_kubeconfig(id).get('config')

if config:
    doc = {}
    doc['metadata'] = {}
    doc['metadata']['doc_type'] = 'application'
    doc['metadata']['application_name'] = 'Kubernetes'
    doc['metadata']['kube_config'] = config

    ret = cdx.actions.hit_action('k8s_add_context',  json.dumps(doc))
    print(ret['stderr'])
    print(ret['stdout'])
    exit(ret['exitcode'])
else:
    print(f"KubeConfig not found for '{id}'")
    exit(1)
# # Check if request was successful
# if response.status_code == 200:
#     print(f"K3s cluster '{id}' was removed")
#     exit(0)
# else:
#     # Return error dictionary
#     print(f"Can't remove k3s cluster '{id}' - ({response.status_code}): {response.content}")
#     exit(1)