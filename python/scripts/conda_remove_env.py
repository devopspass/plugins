import subprocess, sys, json
import cdx

def remove_conda_env(env_name):
    try:
        subprocess.run([cdx.helpers.mamba_bin_path(), 'env', 'remove', '--yes', '-n', env_name], check=True)
        print(f"Removed environment: '{env_name}'")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    ret = json.load(file)
    default_env_name = ret['metadata']['name']

remove_conda_env(default_env_name)
