import subprocess, sys, json, os
import cdx

action = 'conda_init_shell'

def init_deinit_shell(what_to_do, shell):
    if what_to_do == 'Init':
        try:
            ret = subprocess.run([cdx.helpers.mamba_bin_path(), 'shell', 'init', '--shell', shell], check=True, capture_output=True)
            print(f"OK, shell initialized")
            print(ret.stdout.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            exit(1)
    else:
        try:
            ret = subprocess.run([cdx.helpers.mamba_bin_path(), 'shell', 'deinit', '--shell', shell], check=True, capture_output=True)
            print(f"OK, shell removed")
            print(ret.stdout.decode('utf-8'))
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

opts = cdx.helpers.get_action_options(doc, action)
shell = opts.get('shell_name', {}).get('value').split('|')[-1]
what_to_do = opts.get('what_to_do', {}).get('value').split('|')[-1]

init_deinit_shell(what_to_do, shell)