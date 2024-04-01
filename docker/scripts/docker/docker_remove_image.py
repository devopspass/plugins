import docker, json, sys

def remove_image_by_id(image_id):
    """
    Remove a Docker image by ID.

    Parameters:
    - image_id (str): The ID of the Docker image.

    Returns:
    - bool: True if the image was successfully removed, False otherwise.
    """
    try:
        # Create a Docker client
        client = docker.from_env()

        # Remove the image
        client.images.remove(image_id, force=True)

        print(f"Image {image_id} removed successfully.")
        return True

    except docker.errors.ImageNotFound:
        print(f"Image with ID {image_id} not found.")
        return False

    except docker.errors.APIError as e:
        print(f"Error removing image: {e}")
        return False

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

# Example usage:
image_id_to_remove = doc['metadata']['id']

remove_image_by_id(image_id_to_remove)
