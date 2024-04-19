import subprocess
import json
import yaml
import requests
import cdx

def error(msg: str):
    return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': '```' + msg + '```'
            }
        ]

def list():
    ret = []
    # Run the command and capture the output
    output = subprocess.run(['tenv', 'terraform', 'list'], text=True, check=True, capture_output=True)
    for version in output.stdout.split('\n'):
        if version != '':
            if len(version.split('*')) == 1:
                ret.append({"name": version})
            else:
                v = version.split(' ')[1]
                ret.append({"name": v, "active": True})

    return ret
