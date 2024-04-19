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
    output = subprocess.run(['tenv', 'tofu', 'list-remote'], text=True, check=True, capture_output=True)
    for version in output.stdout.split('\n')[1:]:
        if version != '':
            ret.append({"name": version})

    return ret
