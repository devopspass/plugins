import subprocess, sys, json
import cdx

action = 'helm_chart_install'

def install_helm_chart(repo_name, chart_name, vals):
    try:
        cmd = ['helm', 'install']
        for val in vals:
            cmd.append("--set-json")
            cmd.append(f'{val}')

        cmd.append(chart_name)
        cmd.append(repo_name)
        print(' '.join(cmd))
        subprocess.run(cmd, check=True)
        print(f"Installed chart '{repo_name}' as '{chart_name}'")
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
name = opts.get('chart_name', {}).get('value')
vals = opts.get('chart_values', {}).get('value')
vals = vals.split('\n')

# Chart name with repo "bitnami/jenkins"
repo_name = doc['metadata']['name']

install_helm_chart(repo_name, name, vals)
