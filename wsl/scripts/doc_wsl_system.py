import subprocess

def list():
    # Run the 'wsl --list' command and capture the output
    output = subprocess.check_output(['wsl', '--list'], text=True)

    # Parse the output and create a list of dictionaries
    distributions = []
    lines = output.strip().split('\n')[1:]  # Skip the header line
    for line in lines:
        parts = line.split()
        distro_name = parts[0]
        is_default = '*' in parts[1]
        _distro = ' '.join(parts[1:]).replace('*', '').strip()
        distributions.append({
            'name': distro_name,
            'icons': f"assets/icons/os/{_distro}.png",
            'active': is_default,
            'distro': _distro
        })

    return distributions
