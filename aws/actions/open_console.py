import time
import urllib, json, sys
import webbrowser
import requests # 'pip install requests'
import boto3 # AWS SDK for Python (Boto3) 'pip install boto3'
import cdx
import sys

fname_doc = sys.argv[1]
fname_settings = sys.argv[2]

settings = {}

with open(fname_settings, 'r') as file:
    settings = json.load(file)

with open(fname_doc, 'r') as file:
    doc = json.load(file)

opts = cdx.helpers.get_action_options(doc, 'aws_open_console')

profile = doc['metadata']['name']
aws_region =  opts.get('aws_region', {}).get('value')
aws_resource =  opts.get('aws_resource', {}).get('value')
aws_tab = ''

if aws_resource == 'ec2':
    aws_tab = '#Instances:'
if aws_resource == 'dynamodbv2':
    aws_tab = '#tables'
if aws_resource == 'dynamodbv2':
    aws_tab = '#/clusters'
if aws_resource == 'lambda':
    aws_tab = '#/functions'
print(f"Trying to open console for '{profile}/{aws_region}'...\n")

# Step 1: Authenticate user in your own identity system.

# Step 2: Using the access keys for an IAM user in your AWS account,
# call "AssumeRole" to get temporary access keys for the federated user

# Note: Calls to AWS STS AssumeRole must be signed using the access key ID
# and secret access key of an IAM user or using existing temporary credentials.
# The credentials can be in Amazon EC2 instance metadata, in environment variables,
# or in a configuration file, and will be discovered automatically by the
# client('sts') function. For more information, see the Python SDK docs:
# http://boto3.readthedocs.io/en/latest/reference/services/sts.html
# http://boto3.readthedocs.io/en/latest/reference/services/sts.html#STS.Client.assume_role
s = boto3.session.Session(profile_name=profile)
creds = s.get_credentials()
creds = creds.get_frozen_credentials()
# Step 3: Format resulting temporary credentials into JSON
url_credentials = {}
url_credentials['sessionId'] = creds.access_key
url_credentials['sessionKey'] = creds.secret_key
url_credentials['sessionToken'] = creds.token
json_string_with_temp_credentials = json.dumps(url_credentials)

# Step 4. Make request to AWS federation endpoint to get sign-in token. Construct the parameter string with
# the sign-in action request, a 12-hour session duration, and the JSON document with temporary credentials
# as parameters.
request_parameters = "?Action=getSigninToken"
request_parameters += "&SessionDuration=43200"
def quote_plus_function(s):
    return urllib.parse.quote_plus(s)
request_parameters += "&Session=" + quote_plus_function(json_string_with_temp_credentials)

request_url = f"https://signin.aws.amazon.com/federation" + request_parameters

r = requests.get(request_url)
if(r.status_code != 200):
    print(f"Failed to get Sign-In Token - looks like your credentials are expired...")
    exit(2)
# Returns a JSON document with a single element named SigninToken.
signin_token = json.loads(r.text)

# Step 5: Create URL where users can use the sign-in token to sign in to
# the console. This URL must be used within 15 minutes after the
# sign-in token was issued.
request_parameters = "?Action=login"
request_parameters += "&Issuer=Example.org"
request_parameters += "&Destination=" + quote_plus_function(f"https://{aws_region}.console.aws.amazon.com/{aws_resource}/home{aws_tab}")
request_parameters += "&SigninToken=" + signin_token["SigninToken"]
if aws_region:
    request_url = f"https://{aws_region}.signin.aws.amazon.com/federation" + request_parameters
else:
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters

logout_url = f"https://{aws_region}.signin.aws.amazon.com/oauth?Action=logout&redirect_uri={quote_plus_function(request_url)}"
webbrowser.open_new_tab(logout_url)
time.sleep(3)
webbrowser.open_new_tab(request_url)
