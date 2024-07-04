
import json
import sys
import requests

fname_doc = sys.argv[1]

with open(fname_doc, 'r') as file:
    doc = json.load(file)

print(doc)

exit(1)
