import json, yaml, sys
import os
import sys

def get_kubeconfig_path():
    if "KUBECONFIG" in os.environ:
        # If the KUBECONFIG environment variable is set, use its value
        return os.environ["KUBECONFIG"]
    elif os.name == "posix":
        # For Unix-based systems, use the default path
        return os.path.expanduser("~/.kube/config")
    elif os.name == "nt":
        # For Windows, use the default path (update as needed)
        return os.path.join(os.environ["USERPROFILE"], ".kube", "config")
    else:
        # Return None for unsupported OS
        return None

ns = ''

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    ret = json.load(file)
    ns = ret['metadata']['name']

try:
    if not os.path.isfile(get_kubeconfig_path()):
        print(f"KubeConfig at '{get_kubeconfig_path()}' not found")
        exit(1)

    with open(get_kubeconfig_path(), "r") as config_file:
        kubeconfig = yaml.safe_load(config_file)

    contexts = kubeconfig.get('contexts', [])
    current_context = kubeconfig["current-context"]
    if not current_context:
        print('ERROR - Looks like curent context is not set, cant set namespace')
        exit(1)

    # Find the specified context and set it as the default
    i = 0
    for context in kubeconfig.get("contexts", []):
        if context["name"] == current_context:
            kubeconfig['contexts'][i]['context']['namespace'] = ns
            with open(get_kubeconfig_path(), "w") as updated_config_file:
                yaml.dump(kubeconfig, updated_config_file)
            print(f"Namespace '{ns}' set as default")
            exit(0)
        i += 1
    print('Default context not found, can`t set namespace')
    exit(1)

except (KeyError, TypeError):
    print('Error while processing the kubeconfig')
    exit(1)