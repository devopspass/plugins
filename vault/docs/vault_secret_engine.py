import os
import subprocess
import json
import yaml
import requests
import cdx

def error(msg: str):
    return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': '```' + msg + '```'
            }
        ]

def get_vault_token_from_file():
    home_dir = os.path.expanduser('~')
    token_file_path = os.path.join(home_dir, '.vault-token')

    if not os.path.exists(token_file_path):
        raise FileNotFoundError(f"Vault token file not found at {token_file_path}")

    with open(token_file_path, 'r') as token_file:
        token = token_file.read().strip()

    return token

def list_vault_secrets_engines(vault_url, token):
    list_secrets_url = f"{vault_url}/v1/sys/mounts"
    headers = {
        "X-Vault-Token": token
    }
    response = requests.get(list_secrets_url, headers=headers)
    response.raise_for_status()

    secrets_engines = response.json()
    return secrets_engines

def list():
    try:
        token = get_vault_token_from_file()
        if not token:
            return error("Hashicorp Vault Server Address is not set in settings.")

        vault_url = cdx.settings.get('vault.address')

        ses = list_vault_secrets_engines(vault_url, token)
        ret = []
        for se in ses:
            ret.append({
                'name': se,
                'url': f"{vault_url}/ui/vault/secrets/{se}list",
            })
        return ret
    except FileNotFoundError as e:
        return error("Vault token not found at `~/.vault-token`, please do `vault login -method=...`")
