import subprocess, sys, json, os
import cdx

action = 'conda_export_env'

def export_conda_env(env_name, folder):
    try:
        ret = subprocess.run([cdx.helpers.mamba_bin_path(), 'env', 'export', '-n', env_name, '--no-build'], check=True, capture_output=True)
        fname = os.path.join(folder, env_name + '.yml')
        print(f"Exporting environment: '{env_name}' to '{fname}'")

        with open(f"{fname}", 'w') as file:
            file.write(ret.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]


settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)
    env_name = doc['metadata']['name']

# print(doc)
opts = cdx.helpers.get_action_options(doc, action)
# print(opts)
folder = opts.get('env_folder', {}).get('value')
# print(folder)

export_conda_env(env_name, folder)
