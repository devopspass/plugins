import subprocess
import re
import cdx

def list():
    try:
        # Run the command and capture the output
        output = subprocess.check_output(['helm', 'repo', 'list'], text=True)

        # Parse the output to extract environment information
        repos = []
        for line in output.splitlines():
            match = re.match(r'^\s*(.+?)\s+(.+)\s*$', line)
            if match:
                name, url = match.groups()
                if name != "NAME" and name.strip() != "":
                    repos.append({'icon': 'assets/icons/apps/helm.png', 'name': name, 'url': url})

        return repos

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
