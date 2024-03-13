import subprocess
import re
import cdx

def list():
    try:
        # Run the command and capture the output
        output = subprocess.run(['helm', 'repo', 'list'], text=True, check=True, capture_output=True)

        # Parse the output to extract environment information
        repos = []
        for line in output.stdout.splitlines():
            match = re.match(r'^\s*(.+?)\s+(.+)\s*$', line)
            if match:
                name, url = match.groups()
                if name != "NAME" and name.strip() != "":
                    repos.append({'icon': 'assets/icons/apps/helm.png', 'name': name, 'url': url})

        return repos

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
