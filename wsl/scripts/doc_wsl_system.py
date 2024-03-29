import subprocess

def list():
    # Run the 'wsl --list' command and capture the output
    output = subprocess.run(['wsl', '--list'], capture_output=True)

    # Parse the output and create a list of dictionaries
    distributions = []
    lines = output.stdout.decode('utf-8').replace('\x00', '').replace('\r', '').strip().split('\n')[1:]  # Skip the header line
    for line in lines:
        parts = line.split(' ')
        distro_name = parts[0]
        is_default = '(Default)' in parts[-1]
        icon = f"assets/icons/os/linux.png"
        if 'debian' in distro_name.lower():
            icon = f"assets/icons/os/debian.png"
        if 'ubuntu' in distro_name.lower():
            icon = f"assets/icons/os/ubuntu.png"
        if 'kali' in distro_name.lower():
            icon = f"assets/icons/os/kali.png"
        if 'suse' in distro_name.lower() or 'sles' in distro_name.lower():
            icon = f"assets/icons/os/opensuse.png"
        if 'docker' in distro_name:
            icon = f"assets/icons/apps/docker.png"
        distributions.append({
            'name': distro_name,
            'icon': icon,
            'active': is_default,
        })

    return distributions

print(list())