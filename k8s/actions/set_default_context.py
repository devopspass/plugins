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

ctx = ''

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    ret = json.load(file)
    ctx = ret['metadata']['name']

try:
    if not os.path.isfile(get_kubeconfig_path()):
        exit(1)

    with open(get_kubeconfig_path(), "r") as config_file:
        kubeconfig = yaml.safe_load(config_file)

    # Find the specified context and set it as the default
    for context in kubeconfig.get("contexts", []):
        if context["name"] == ctx:
            kubeconfig["current-context"] = ctx
            with open(get_kubeconfig_path(), "w") as updated_config_file:
                yaml.dump(kubeconfig, updated_config_file)
            print(f"Context '{ctx}' set as default")
            exit(0)
    print('Context not found')
    exit(1)

except (KeyError, TypeError):
    print('Error while processing the kubeconfig')
    exit(1)