import json
import sys
import webbrowser
import os

url = ''

try:
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        fname_doc = sys.argv[1]
        doc = {}

        with open(fname_doc, 'r') as file:
            doc = json.load(file)
        url = doc.get('metadata', {}).get('url', '').strip('\n')
except Exception as e:
    print(e)

print(f"Openning URL")
print(url)
webbrowser.open_new_tab(url)
