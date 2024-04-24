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

import requests
import re

def list():
    url = 'https://ollama.com/library'

    # # Send GET request to the URL
    response = requests.get(url)
    res = []
    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Extract content from response
        html_content = response.text

        # Define regular expressions to extract information
        pattern = r'.*?<p class=".*?">(.*?)<\/p>.*?<span.*?>\s*([\d\.]+)\s*Pulls.*?<\/span>.*?<span.*?>\s*([\d\.]+)\s*Tags.*?<\/span>.*?<span.*?>\s*Updated\s*(.*?)\s*ago<\/span>'
        # for line in html_content.split("\n"):
        match = re.findall(r'<h2.*?>(.*?)<\/h2>.*?<p class.*?>(.*?)<\/p>', html_content, re.DOTALL)
        print(match)
        if match:
            for m in match:
                name = m[0]
                desc = m[1]
                res.append({"name": name.strip(), "description": desc})
    return res
