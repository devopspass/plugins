import docker
import time, json, sys

def force_remove_container(container_id):
    """
    Forcefully stop a Docker container after the specified duration.

    Parameters:
    - container_id (str): The ID or name of the Docker container.
    - timeout_seconds (int): The duration in seconds before forcefully stopping the container.

    Returns:
    - bool: True if the container was successfully stopped, False otherwise.
    """
    client = docker.from_env()

    try:
        # Stop the container gracefully first
        client.containers.get(container_id).remove(force=True)

        return True
    except docker.errors.NotFound:
        print(f"Container '{container_id}' not found.")
        exit(1)
    except docker.errors.APIError as e:
        print(f"Error removing container '{container_id}': {e}")
        exit(1)


fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

container_id_to_remove = doc['metadata']['name']

# Call the function with the container ID and optional timeout (default is 10 seconds)
success = force_remove_container(container_id_to_remove)

if success:
    print(f"Container '{container_id_to_remove}' removed successfully.")
else:
    print(f"Failed to remove container '{container_id_to_remove}'.")
    exit(1)
