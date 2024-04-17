import sys, json
import webbrowser

from kubernetes import client, config
from kubernetes.client.rest import ApiException

def get_console_url(context):
    # Load kubeconfig and initialize Kubernetes client
    config.load_kube_config(context=context)
    v1 = client.CoreV1Api()

    # Specify the namespace and the name of the ConfigMap
    namespace = 'openshift-config-managed'
    configmap_name = 'console-public'

    try:
        # Get the ConfigMap
        configmap = v1.read_namespaced_config_map(name=configmap_name, namespace=namespace)

        # Extract the consoleURL data from the ConfigMap
        console_url = configmap.data.get('consoleURL')

        return console_url
    except ApiException as e:
        if e.status == 404:
            print("Web Console supported only for OpenShift clusters")
        else:
            print("Exception when calling CoreV1Api->read_namespaced_config_map:", e)
        return None

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

# Example usage
context = doc['metadata']['name']

console_url = get_console_url(context)
if console_url:
    print("Console URL: ", console_url)
else:
    print("Failed to retrieve console URL")
    exit(1)

webbrowser.open_new_tab(console_url)
