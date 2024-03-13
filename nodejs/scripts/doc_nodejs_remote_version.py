import subprocess
import re
import subprocess

def list():
    ret = []
    try:
        # Run 'nvm list' command in a shell
        output = subprocess.check_output(['bash', '-c', 'source ~/.nvm/nvm.sh && nvm ls-remote node --no-colors'], text=True)
        # Process the output as needed
        node_versions = output.split('\n')
        for version in node_versions:
            match = re.match(r'\s*([\w\.-_]+)\s*(\(.*\))?.*', version)
            if match:
                ver, comment = match.groups()
                ret.append({'icon': 'assets/icons/apps/nodejs.png', 'name': ver, 'comment': comment})

        return ret

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
