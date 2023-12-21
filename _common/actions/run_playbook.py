import subprocess
import sys
import json, os, yaml
import tempfile

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]
with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

home_path = os.path.join(os.path.expanduser("~"), '.devopspass-ai')
env_path = os.path.join(home_path, 'mamba', 'envs', 'codex')
if sys.platform == "win32":
    python_bin_path = os.path.join(env_path, 'python.exe')
else:
    python_bin_path = os.path.join(env_path, 'bin', 'python')


os.environ['ANSIBLE_STDOUT_CALLBACK'] = 'yaml'
os.environ['ANSIBLE_DIFF_ALWAYS'] = 'true'
os.environ['ANSIBLE_FORCE_COLOR'] = 'true'
#os.environ['PYTHONDEBUG'] = 'true'
#os.environ['PYTHONVERBOSE'] = 'true'

ret = {}
for key, value in doc.get('metadata',{}).get('values', {}).items():
    _k = key.replace('.', '_')
    ret[_k] = value

ret['ansible_python_interpreter'] = python_bin_path

pl = doc.get('metadata',{}).get('playbook')

if doc.get('metadata',{}).get('by_user'):
    pl = os.path.join(home_path, pl)
else:
    pl = os.path.join(os.getcwd(), pl)


result = subprocess.run(
    [
        python_bin_path,
        '-m',
        'ansible',
        'playbook',
        '--diff',
        '-l',
        'localhost',
        '-i',
        'localhost,',
        '-e',
        json.dumps(ret),
        pl
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

print(result.stdout)
print(result.stderr)

if result.returncode != 0:
    print("Failed to execute action.")
    exit(1)
