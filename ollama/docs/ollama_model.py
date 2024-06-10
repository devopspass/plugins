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

def list():
    # Kick API and return result
    #
    url = cdx.settings.get('ollama.server')

    try:
        resp = requests.get(url + "/api/tags")
        if resp.status_code == 200:
            ret = []
            for model in resp.json().get("models", []):
                m = {}
                m['name'] = model['name']
                m['model'] = model['model']
                m['size'] = f"{round(model['size'] / (1024 * 1024), 1)} Mb",
                m['parent'] = model['details']['parent_model']
                m['paramenters'] = model['details']['parameter_size']
                m['q'] = model['details']['quantization_level']
                ret.append(m)
            return ret
        else:
            return error(f"Something went wrong: {resp.content}")
    except Exception as e:
        return error(f"{e}")
