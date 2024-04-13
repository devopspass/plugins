import subprocess
import re, json, os
import cdx
import botocore.session

def list():
    aws = []

    session = botocore.session.get_session()
    profiles = session.available_profiles

    for p in profiles:
        aws.append(
            {
                'name': p,
            }
        )

    aws = sorted(aws, key=lambda p: p['name'])
    return aws
