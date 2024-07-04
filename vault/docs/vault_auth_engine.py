import subprocess
import json
import cdx

def list():
    try:
        # Run the command and capture the output
        output = subprocess.run(['vault', 'auth', 'list', '-format', 'json'], text=True, capture_output=True, check=True)
        ret = []
        # Parse the output to extract environment information
        auth_engines = json.loads(output.stdout)
        print(auth_engines.keys())
        for engine in auth_engines:
            # release['icon'] = 'assets/icons/' + get_icon(release['name'])
            ret.append({
                'name': engine,
                'type': auth_engines[engine].get('type'),
                'description': auth_engines[engine].get('description'),
                })

        return ret

    except FileNotFoundError as e:
        return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': f"Can't find 'vault' in PATH, looks like its not installed, please install first"
            }
        ]
