
import json
import sys
import requests

fname_doc = sys.argv[1]

with open(fname_doc, 'r') as file:
    doc = json.load(file)

print(doc)

token = doc['aws_sso_token']
url = f'https://portal.sso.us-east-1.amazonaws.com/token/whoAmI'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'x-amz-sso-bearer-token': token,
    'x-amz-sso_bearer_token': token,
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("AWS SSO: token works")
    exit(0)
else:
    print("AWS SSO: token doesn't work")
    exit(1)
