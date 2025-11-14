import subprocess
import json
import yaml
import requests
import cdx

def list_docs():
    base_url = cdx.settings.get('gitlab.server')
    bearer_token = cdx.settings.get('gitlab.token')

    if not base_url or not bearer_token:
        return error("Please specify GitLab server URL and token in Settings.")
    
    # Retreive all repos users has access to
    url = f"{base_url.rstrip('/')}/api/v4/projects?membership=true&per_page=100"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    projects = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return error(f"Failed to retrieve projects: {response.text}")
        
        projects.extend(response.json())
        
        # Check for next page in headers
        url = response.links.get('next', {}).get('url')

    ret = []
    for project in projects:
        ret.append({
            'name': project.get('name'),
            'url': project.get('web_url'),
            'description': project.get('description') or '',
            'ssh_url_to_repo': project.get('ssh_url_to_repo'),
            'visibility': project.get('visibility'),
            'name_with_namespace': project.get('name_with_namespace'),
            # Markdown formated list of links to commits, MRs, issues, pipelines
            'links': f"""
- [Pipelines]({project.get('web_url')}/-/pipelines)
- [MRs]({project.get('web_url')}/-/merge_requests)
- [Commits]({project.get('web_url')}/-/commits)
- [Branches]({project.get('web_url')}/-/branches)
- [Tags]({project.get('web_url')}/-/tags)
- [Releases]({project.get('web_url')}/-/releases)
- [Issues]({project.get('web_url')}/-/issues)
            """,
        })
    return ret