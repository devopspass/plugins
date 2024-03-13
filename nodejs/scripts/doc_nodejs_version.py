import subprocess
import re
import subprocess

def list():
    ret = []
    try:
        # Run 'nvm list' command in a shell
        output = subprocess.check_output(['bash', '-c', '. ~/.nvm/nvm.sh && nvm list node --no-colors'], text=True)
        # Process the output as needed
        node_versions = output.split('\n')
        for version in node_versions:
            match = re.match(r'.*(->)?\s+([\w\.-_]+)', version)
            if match:
                active, ver = match.groups()
                ret = [{'icon': 'assets/icons/apps/nodejs.png', 'active': ('->' in version), 'name': ver}] + ret

        return ret

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
