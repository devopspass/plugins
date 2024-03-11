import subprocess
import re
import cdx

def list():
    try:
        # Run the command and capture the output
        output = subprocess.check_output([cdx.helpers.mamba_bin_path(), 'env', 'list'], text=True)

        # Parse the output to extract environment information
        envs = []
        for line in output.splitlines():
            match = re.match(r'^\s*(.+?)\s+([\*]*)\s+(.*)$', line)
            if match:
                name, active, path = match.groups()
                if name != "Name" and name.strip() != "":
                    envs.append({'icon': 'assets/icons/apps/conda.png', 'name': name, 'active': active.strip() == '*', 'path': path.strip()})

        return envs

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
