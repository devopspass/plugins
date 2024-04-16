import os, sys
import yaml, json
import webbrowser
import cdx

def helm_cache_path():
    """
    Returns the path to the Helm cache folder.
    """
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Check if the HELM_CACHE_HOME environment variable is set
    cache_home = os.environ.get("HELM_CACHE_HOME")

    if cache_home:
        # If HELM_CACHE_HOME is set, use it as the cache folder
        cache_path = os.path.join(cache_home, "repository")
    else:
        # Otherwise, use the default cache folder in the user's home directory
        if cdx.helpers.is_linux():
            cache_path = os.path.join(home_dir, ".cache", "helm", "repository")

        if cdx.helpers.is_macos():
            cache_path = os.path.join(home_dir, "Library", "Caches", "helm", "repository")
        if cdx.helpers.is_windows():
            cache_path = os.path.join(os.environ['TEMP'], "helm", "repository")

    return cache_path

def get_chart_sources(repo_chart_str):
    """
    Retrieves the list of sources for the specified chart in the Helm cache.

    Args:
    - repo_chart_str (str): A string in the format "REPO/CHART".

    Returns:
    - List: A list of sources for the specified chart.
    """
    # Split the repo/chart string
    repo, chart = repo_chart_str.split("/")

    # Get the path to the Helm cache folder
    cache_folder = helm_cache_path()

    # Construct the path to the index.yaml file
    index_file = os.path.join(cache_folder, f"{repo}-index.yaml")

    # Check if the index file exists
    if not os.path.exists(index_file):
        return []

    # Open the YAML file for reading
    with open(index_file, 'r') as f:
        # Initialize variables
        found = False
        wait_end = False
        piece = ""

        # Read the file line by line
        for line in f:
            # Check if the current line contains "airflow:"
            if f" {chart}:" in line:
                found = True
                piece += line
            # Check if we are in the airflow entry
            elif found:
                # Check if we have reached the end of the airflow entry
                if line.startswith("  -") and wait_end:
                    break
                else:
                    # Concatenate the line to the piece
                    piece += line
                wait_end = True
    index_data = yaml.safe_load(piece)

    # Get the sources for the specified chart
    sources = index_data[chart][0].get('sources', [])

    return sources


action = 'helm_open_chart_sources'

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

name = doc['metadata']['name']

chart_sources = get_chart_sources(name)
print("Sources for chart:", chart_sources)

if len(chart_sources) == 0:
    print("ERROR: Sources URL not found")
    exit(1)
else:
    webbrowser.open_new_tab(chart_sources[0])
