import subprocess
import re, json
import cdx

def list():
    try:
        # Run the command and capture the output
        output = subprocess.run(['docker', 'compose', 'ls', '--format', 'json'], text=True, check=True, capture_output=True)

        # Parse the output to extract environment information
        repos = json.loads(output.stdout)
        ret = []
        for repo in repos:
            r = {}
            r['icon'] = 'assets/icons/apps/docker.png'
            for k in repo.keys():
                r[k.lower()] = repo[k]
            ret.append(r)

        return ret

    except subprocess.CalledProcessError as e:
        return [{'name': 'ERROR', 'icon': 'assets/icons/general/error.png', 'error': f"{e}\n{e.output}\n{e.stderr}"}]
    except FileNotFoundError as e:
        return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': f"Can't find 'docker' in PATH, looks like its not installed, please install first"
            }
        ]
