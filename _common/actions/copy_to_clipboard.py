from pandas.io import clipboard
import sys
import json

fname_doc = sys.argv[1]
doc = {}

with open(fname_doc, 'r') as file:
    doc = json.load(file)
val = doc.get('metadata', {}).get('text', '').strip('\n')

def _copy(val):
    clipboard.copy(val)

_copy(val)
print(f"Copied to clipboard '{val}'")
exit(0)