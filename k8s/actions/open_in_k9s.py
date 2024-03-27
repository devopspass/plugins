import subprocess, sys, json

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

cmd = settings['terminal.command']
name = doc['metadata']['name']
doc_type = doc['metadata']['doc_type']

# Command to run k9s with the specified context and namespace
k9s_command = f"k9s"

if doc_type == 'k8s_context':
    k9s_command += f" --context {name}"
elif doc_type == 'k8s_namespace':
    k9s_command += f" --namespace {name}"

# Command to open a new GNOME Terminal window and run k9s

command = cmd.replace('%COMMAND%', k9s_command)

print(command)

# Run the command in a new terminal window
subprocess.Popen(command, shell=True)
