import webbrowser, sys, json

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

port = settings['autok3s.port']

print("Opening K3s endpoint...")
webbrowser.open_new_tab(f'http://127.0.0.1:{port}/')
