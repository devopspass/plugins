import json
import subprocess
import re
import cdx

def list():
    try:
        # Run the command and capture the output
        output = subprocess.run(['helm', 'repo', 'list', '-o', 'json'], text=True, check=True, capture_output=True)
        return json.loads(output.stdout)

    except subprocess.CalledProcessError as e:
        return [{'name': 'ERROR', 'icon': 'assets/icons/general/error.png', 'error': f"{e}\n{e.output}\n{e.stderr}"}]
    except FileNotFoundError as e:
        return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': f"Can't find 'helm' in PATH, looks like its not installed, please install first"
            }
        ]
