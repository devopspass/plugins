import subprocess, sys, json
import webbrowser
import cdx

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    ret = json.load(file)

name = ret['metadata']['name']
try:
    url = "https://ollama.com/library/" + name
    webbrowser.open_new_tab(url)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    exit(1)
