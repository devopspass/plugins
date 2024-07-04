import re
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
    try:
        # Run the command and capture the output
        output = subprocess.run(['argocd', 'app', 'list', '-o', 'json'], text=True, check=True, capture_output=True)

        # Parse the output to extract environment information
        apps = []
        apps = json.loads(output.stdout)
        for app in apps:
            a = {
                'name': app.get('metadata', {}).get('name'),
            }
            apps.append(a)

        return apps

    except subprocess.CalledProcessError as e:
        return [{'name': 'ERROR', 'icon': 'assets/icons/general/error.png', 'error': f"{e}\n{e.output}\n{e.stderr}"}]
    except FileNotFoundError as e:
        return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': f"Can't find 'argocd' in PATH, looks like its not installed, please install first"
            }
        ]
