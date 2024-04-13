import json, sys, subprocess, re
import cdx
import yaml
import tempfile

action = 'conda_create_env'
fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

opts = cdx.helpers.get_action_options(doc, action)
name = opts.get('conda_env_name', {}).get('value')
channels = opts.get('conda_channels', {}).get('value')
packages = opts.get('packages', {}).get('value')
env_raw = opts.get('env_raw', {}).get('value')
pip = opts.get('pip', {}).get('value')

def create_conda_environment(name, packages, channels, env_raw, pip):
    """
    Create a Conda environment based on the provided arguments.

    Parameters:
    - name (str): Name of the Conda environment.
    - packages (list): List of Conda packages.
    - env_raw (str): Conda environment description.
    - pip (list): List of pip packages.

    Returns:
    - bool: True if the Conda environment was successfully created, False otherwise.
    """
    # Create a temporary YAML file with the Conda environment description
    temp_yaml_file = ''

    env_data = {"name": name, "channels": channels, "dependencies": packages}
    if len(pip) > 0:
        env_data['dependencies'].append({'pip': pip})

    if env_raw.strip() != '':
        env_data = yaml.safe_load(env_raw)
        env_data['name'] = name

    with tempfile.NamedTemporaryFile('w', suffix='.yml') as yaml_file:
        yaml.dump(env_data, yaml_file, default_flow_style=False)
        print(f"'{yaml_file.name}'")
        temp_yaml_file = yaml_file.name

        try:
            # Run "conda env create" using the generated YAML file
            subprocess.run([cdx.helpers.mamba_bin_path(), 'env', 'create', '--yes', '-f', temp_yaml_file], check=True)
            print(f"Conda environment '{name}' created successfully.")
            exit(0)
        except subprocess.CalledProcessError as e:
            print(f"Error creating Conda environment: {e}")
            exit(1)
        finally:
            # Clean up: Remove the temporary YAML file
            # REMOVE temp_yaml_file
            x = ''

create_conda_environment(
    name=name,
    packages=list(map(str.strip, packages.split(','))),
    channels=list(map(str.strip, channels.split(','))),
    env_raw=env_raw,
    pip=re.findall(r'^([\w-]+==[\d.]+)', pip, flags=re.MULTILINE)
)

