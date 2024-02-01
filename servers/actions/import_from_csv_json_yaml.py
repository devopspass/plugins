import json
import yaml
import csv
import sys, os
import cdx
from cdx.servers import ServerManager

from pathlib import Path

def process_file(file_path):
    file_extension = Path(file_path).suffix[1:].lower()

    with open(file_path, 'r') as file:
        if file_extension == 'json':
            data = json.load(file)
        elif file_extension in ['yaml', 'yml']:
            data = yaml.safe_load(file)
        elif file_extension == 'csv':
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    manager: ServerManager = ServerManager(os.path.join(cdx.helpers.dop_home_path(), 'server_database.db'))

    created = 0
    updated = 0

    # Call create_server function for each record in data
    for record in data:
        res = manager.create_server(record)
        if res == ServerManager.CREATED:
            created += 1
        else:
            updated += 1

    print(f"OK: Import finished - {created} server(s) added, {updated} server(s) updated")


fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

fname = doc.get('metadata', {}).get('actions', [])[0].get('required_options', {}).get('file_name', {}).get('value')

# Example usage:
process_file(fname)
