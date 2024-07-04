from kubernetes import client, config
from kubernetes.client.rest import ApiException
import urllib3

def error(msg: str):
    return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': msg
            }
        ]

def list():
    # Load Kubernetes configuration from default location
    config.load_kube_config()

    contexts = config.list_kube_config_contexts()
    d_name = contexts[1].get('name')
    current_context = None
    for c in contexts[0]:
        if d_name == c.get('name', ''):
            current_context = c
            break
    if not current_context:
        return {'name': 'ERROR', 'message': 'Looks like KubeConfig is invalid or did not exist'}

    current_namespace = current_context.get('context', {}).get('namespace', 'default')
    # Create an instance of the Kubernetes client
    v1 = client.CoreV1Api()

    # Retrieve list of namespaces
    try:
        namespaces = v1.list_namespace()
    except ApiException as e:
        if e.status == 403:
            from kubernetes import dynamic
            from kubernetes.client import api_client
            c = dynamic.DynamicClient(
                api_client.ApiClient(configuration=config.load_kube_config())
            )
            namespaces = c.resources.get(api_version="project.openshift.io/v1", kind="Project").get()
        if e.status == 401:
            return error("401: " + e.reason)
        else:
            raise(e)
    except urllib3.exceptions.MaxRetryError:
        return error(f"Failed to connect Kubernetes cluster '{d_name}'")

    # Extract namespace names and their status
    namespace_info = []
    for namespace in namespaces.items:
        namespace_name = namespace.metadata.name
        namespace_active = namespace_name == current_namespace
        namespace_info.append({"name": namespace_name, "context": current_context.get("name"), "active": namespace_active})

    return namespace_info
