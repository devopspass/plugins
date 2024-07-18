import re
import requests
import os
import json
import cdx

def error(msg: str):
    return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': msg
            }
        ]

def convert_jira_to_markdown(jira_text):
    # Convert headings
    jira_text = re.sub(r'h([1-6])\.\s', lambda m: '#' * int(m.group(1)) + ' ', jira_text)

    # Convert bold text
    jira_text = re.sub(r'\*(.*?)\*', r'**\1**', jira_text)

    # Convert italic text
    jira_text = re.sub(r'_(.*?)_', r'*\1*', jira_text)

    # Convert bullet lists
    jira_text = re.sub(r'^\* ', r'* ', jira_text, flags=re.MULTILINE)

    # Convert numbered lists
    jira_text = re.sub(r'^\s*# ', r'1. ', jira_text, flags=re.MULTILINE)

    # Convert links
    jira_text = re.sub(r'\[(.*?)\|(http[s]?:\/\/[^\]]+)\]', r'[\1](\2)', jira_text)

    # Convert code blocks
    jira_text = re.sub(r'\{code:([^\}]*)\}\n', r'```\1\n', jira_text)
    jira_text = re.sub(r'\{code\}', r'```', jira_text)

    jira_text = re.sub(r'\{noformat\}', '`', jira_text)

    return jira_text

def list():
    jira_server = cdx.settings.get('jira.server')
    jira_server = jira_server.rstrip('/')

    jira_token = cdx.settings.get('jira.token')
    jql_query = cdx.settings.get('jira.jql_query')

    if not jira_server or not jira_token:
        return error('JIRA credentials are not set in Settings')

    if jql_query is None:
        jql_query = 'assignee = currentUser() and statusCategory != Done'

    # JIRA REST API endpoint for searching issues
    search_url = f"{jira_server}/rest/api/2/search"
    headers = {
        'Authorization': f'Bearer {jira_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'jql': jql_query,
        'maxResults': 50,  # Adjust as needed
        'fields': 'key,summary,status,assignee,priority,description,created,updated,labels,reporter'
    }

    # Perform the request
    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve JIRA issues: {response.status_code} - {response.text}")

    print(response.content)

    issues = response.json().get('issues', [])

    stories = []
    for issue in issues:
        stories.append({
            'name': issue.get('key'),
            'url': jira_server + '/browse/' + issue.get('key'),
            'summary': issue.get('fields', {}).get('summary'),
            'status': "`" + issue.get('fields', {}).get('status', {}).get('name') + "` ",
            'assignee': issue.get('fields', {}).get('assignee', {}).get('displayName'),
            'reporter': issue.get('fields', {}).get('reporter', {}).get('displayName'),
            # 'priority': issue.fields.priority.name if issue.fields.priority else None,
            'description': convert_jira_to_markdown(str(issue.get('fields', {}).get('description', ''))),
            # 'created': issue.fields.created,
            # 'updated': issue.fields.updated,
            # 'labels': issue.fields.labels,
        })

    return stories
