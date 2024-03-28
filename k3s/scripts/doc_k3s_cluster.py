import requests

port = "8080"

def list():
    url = f"http://127.0.0.1:{port}/v1/clusters"
    # Send GET request to fetch clusters data
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse response and get required information
        clusters_info = parse_clusters_response(response)
        return clusters_info
    else:
        # Return error dictionary
        error_msg = f"Can't reach autok3s at '{url}' - ({response.status_code}): {response.content}"
        return [{
            'name': 'ERROR',
            'icon': 'assets/icons/general/error.png',
            'error': error_msg
        }]

def parse_clusters_response(response):
    # Parse JSON response
    clusters_data = response.json()["data"]

    # Initialize list to store parsed data
    parsed_clusters = []

    # Iterate over clusters data and extract required information
    for cluster_data in clusters_data:
        cluster_name = cluster_data["name"]
        id = cluster_data['id']
        cluster_provider = cluster_data['provider']
        if cluster_provider == 'k3d':
            provider_icon = f"assets/icons/k8s/k3s.png"
        else:
            provider_icon = f"assets/icons/cloud/{cluster_provider}.png"
        masters = int(cluster_data["master"])
        workers = int(cluster_data["worker"])
        status = cluster_data["status"]
        url = f"http://127.0.0.1:{port}/ui/cluster-explorer/core/clusters/detail/{id}"

        # Append parsed data to the list
        parsed_clusters.append({
            "icon": provider_icon,
            "name": cluster_name,
            "id": id,
            "type_title": cluster_provider,
            "masters": masters,
            "workers": workers,
            "status": status,
            "url": url,
        })

    return parsed_clusters
