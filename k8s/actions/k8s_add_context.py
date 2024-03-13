import json, sys, os, yaml
import cdx

action = 'k8s_add_context'
fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

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


settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

opts = cdx.helpers.get_action_options(doc, action)
new_config = yaml.safe_load(opts.get('kube_config', {}).get('value'))

# apiVersion: v1
# clusters:
# - cluster:
#     certificate-authority-data: ...
#     server: https://0.0.0.0:36725
#   name: k3d-local
# contexts:
# - context:
#     cluster: k3d-local
#     user: admin@k3d-local
#   name: k3d-local
# current-context: k3d-local
# kind: Config
# preferences: {}
# users:
# - name: admin@k3d-local
#   user:
#     client-certificate-data: ...
#     client-key-data: ...

def merge_sections(key: str, new_config, current_config):
    res = dict(current_config)
    res[key] = []

    if len(new_config.get(key, [])) == 0:
        res[key] = current_config[key]
    else:
        for _section in new_config.get(key, []):
            for section in current_config.get(key, []):
                if section['name'] == _section['name']:
                    res[key].append(_section)
                else:
                    res[key].append(section)
    return res

try:
    current_config = {
        'kind': 'Config',
        'apiVersion': 'v1',
        'clusters': [],
        'contexts': [],
        'users': [],
        'current-context': '',
        'preferences': {}
    }

    if os.path.isfile(get_kubeconfig_path()):
        with open(get_kubeconfig_path(), "r") as config_file:
            current_config = yaml.safe_load(config_file)
    else:
        print(f"KubeConfig at '{get_kubeconfig_path()}' not found, creating")

    # Add/update contexts
    current_config = merge_sections('contexts', new_config, current_config)
    current_config = merge_sections('clusters', new_config, current_config)
    current_config = merge_sections('users', new_config, current_config)

    # Save changes
    with open(get_kubeconfig_path(), "w") as updated_config_file:
        yaml.dump(current_config, updated_config_file)
        print("KubeConfig successfully updated.")

except (KeyError, TypeError) as e:
    print(f'Error while processing the kubeconfig: {e}')
    exit(1)