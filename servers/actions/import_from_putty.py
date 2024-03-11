import subprocess

registry_key = "HKEY_CURRENT_USER\Software\SimonTatham\PuTTY"

try:
    result = subprocess.run(['reg', 'query', registry_key], capture_output=True, text=True, check=True)
    output_lines = result.stdout.splitlines()
    for line in output_lines:
        print(line)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
