import os, json
import sys
import cdx

action = 'docker_open_image_description'

def get_docker_hub_url(image_name):
    """
    Get the Docker Hub URL for a given Docker image name.

    Parameters:
    - image_name (str): The Docker image name.

    Returns:
    - str: The Docker Hub URL for the given image name.
    """
    # Docker Hub base URL
    docker_hub_base_url = "https://hub.docker.com"

    # Split the image name into components (registry, namespace, repository, tag)
    parts = image_name.split('/')

    # Replace ':' with '_' in the tag to handle multi-part tags
    tag = parts[-1].split(':')[0]

    # If the image name includes a registry and/or namespace, use them in the URL
    if len(parts) > 1:
        registry_namespace_url_safe = '_'.join(parts[:-1])
        docker_hub_url = f"{docker_hub_base_url}/r/{registry_namespace_url_safe}/{tag}"
    else:
        docker_hub_url = f"{docker_hub_base_url}/_/{tag}"

    return docker_hub_url


fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

# opts = cdx.helpers.get_action_options(doc, action)
image_name = doc['metadata']['name']

plugin_path = os.path.join(cdx.helpers.plugins_path(), '_common/actions/open_url.py')
cmd = f"{cdx.helpers.python_bin_path()} {plugin_path} '{get_docker_hub_url(image_name)}'"
os.system(cmd)
