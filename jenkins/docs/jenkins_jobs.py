import subprocess
import json
import yaml
import requests
import cdx
import jenkins

# Example usage:
def error(msg: str):
    return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': '```' + msg + '```'
            }
        ]

def list():
    res = []
    jenkins_url, user, token = cdx.settings.get('jenkins.server').split('|')
    server = jenkins.Jenkins(jenkins_url, username=user, password=token)
    _res = []
    try:
        jobs = server.get_jobs()
        for job in jobs:
            if job.get('jobs'):
                for j in job.get('jobs'):
                    _res.append(j)
            else:
                _res.append(job)

        for r in _res:
            if 'anime' in r.get('color', []):
                icon = r['color'] + ".gif"
            else:
                icon = r['color'] + ".png"
            if 'notbuilt' in r['color']:
                icon = icon.replace("not", "no")
            r['icon'] = "https://raw.githubusercontent.com/jenkinsci/jenkins/master/war/src/main/webapp/images/32x32/" + icon
            del r['color']
            res.append(r)
    except requests.exceptions.RequestException as e:
        return error("Could not connect to Jenkins - " + str(e))
    return res

