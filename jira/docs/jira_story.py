import re
import requests
import os
import json
import base64
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

# detect ADF description and convert; includes ADF -> Markdown converter
def convert_adf_to_markdown(adf_doc):
    def apply_marks(text, marks):
        if not marks:
            return text
        for m in marks:
            t = m.get('type')
            attrs = m.get('attrs', {}) if isinstance(m, dict) else {}
            if t == 'strong':
                text = f"**{text}**"
            elif t == 'em':
                text = f"*{text}*"
            elif t == 'code':
                text = f"`{text}`"
            elif t == 'strike' or t == 'strikethrough':
                text = f"~~{text}~~"
            elif t == 'link':
                href = attrs.get('href', '')
                text = f"[{text}]({href})"
        return text

    def render_node(node, indent=0, list_kind=None):
        ntype = node.get('type')
        if ntype == 'text':
            return apply_marks(node.get('text', ''), node.get('marks'))
        if ntype == 'paragraph':
            inner = ''.join(render_node(c, indent) for c in node.get('content', []))
            return inner.rstrip() + '\n\n'
        if ntype == 'heading':
            level = node.get('attrs', {}).get('level', 1)
            inner = ''.join(render_node(c, indent) for c in node.get('content', []))
            return ('#' * level) + ' ' + inner.rstrip() + '\n\n'
        if ntype == 'codeBlock':
            lang = node.get('attrs', {}).get('language', '')
            text = ''.join(c.get('text', '') for c in node.get('content', []))
            return f"```{lang}\n{text.rstrip()}\n```\n\n"
        if ntype == 'blockquote':
            text = ''.join(render_node(c, indent) for c in node.get('content', []))
            lines = [("> " + l) if l.strip() else ">" for l in text.splitlines()]
            return '\n'.join(lines).rstrip() + '\n\n'
        if ntype == 'hardBreak':
            return '  \n'
        if ntype == 'rule':
            return '---\n\n'
        if ntype in ('bulletList', 'orderedList'):
            kind = 'ordered' if ntype == 'orderedList' else 'bullet'
            items = ''.join(render_node(c, indent + 1, list_kind=kind) for c in node.get('content', []))
            return items + '\n'
        if ntype == 'listItem':
            inner = ''.join(render_node(c, indent, list_kind) for c in node.get('content', []))
            inner = inner.rstrip().replace('\n\n', '\n')
            prefix = ('1. ' if list_kind == 'ordered' else '- ')
            return ('  ' * (max(indent - 1, 0))) + prefix + inner + '\n'
        if ntype == 'mention':
            attrs = node.get('attrs', {})
            return attrs.get('text') or f"@{attrs.get('id','')}"
        if ntype == 'image':
            attrs = node.get('attrs', {})
            src = attrs.get('src') or attrs.get('url') or ''
            alt = attrs.get('alt') or ''
            return f"![{alt}]({src})"
        if ntype == 'inlineCard':
            attrs = node.get('attrs', {})
            url = attrs.get('url', '')
            title = attrs.get('title', url)
            return f"[{title}]({url})"
        # Fallback: render children if any
        if 'content' in node:
            return ''.join(render_node(c, indent) for c in node.get('content', []))
        return ''

    if not isinstance(adf_doc, dict):
        return ''
    # ADF root is usually type "doc" with "content"
    content = adf_doc.get('content', [])
    md = ''.join(render_node(n, indent=0) for n in content)
    # tidy up excess whitespace
    return md.strip() + '\n' if md.strip() else ''

def list_docs():
    jira_server = cdx.settings.get('jira.server')
    jira_token = cdx.settings.get('jira.token')

    if not jira_server or not jira_token:
        return error('JIRA credentials are not set in Settings')

    jira_server = jira_server.rstrip('/')
    jql_query = cdx.settings.get('jira.jql_query')

    if jql_query is None:
        jql_query = 'assignee = currentUser() and statusCategory != Done'
    # JIRA REST API endpoint for searching issues
    search_url = f"{jira_server}/rest/api/3/search/jql"

    # Jira Cloud expects Basic auth with email:api_token (API token) — encode as base64
    jira_user = cdx.settings.get('jira.user') or cdx.settings.get('jira.email')
    if not jira_user:
        return error('JIRA user/email is not set in Settings; Jira Cloud requires email + API token for Basic auth')

    # Encode email:api_token for Basic auth when using Jira Cloud API token
    token_bytes = f"{jira_user}:{jira_token}".encode('utf-8')
    basic_token = base64.b64encode(token_bytes).decode('ascii')

    headers = {
        'Authorization': f'Basic {basic_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'jql': jql_query,
        'maxResults': 50,  # Adjust as needed
        'fields': 'key,summary,status,assignee,priority,description,created,updated,labels,reporter',
        "fieldsByKeys": True
    }

    # Perform the request
    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve JIRA issues: {response.status_code} - {response.text}")

    print(response.content)

    issues = response.json().get('issues', [])

    stories = []
    for issue in issues:
        # inside the loop: decide which converter to use
        desc_field = issue.get('fields', {}).get('description')
        if isinstance(desc_field, str):
            try:
                desc_field = json.loads(desc_field.decode('utf-8')) if isinstance(desc_field, bytes) else json.loads(desc_field)
            except json.JSONDecodeError:
                desc_field = desc_field
        if isinstance(desc_field, dict) and desc_field.get('type') == 'doc':
            desc = convert_adf_to_markdown(desc_field)
        else:
            desc = convert_jira_to_markdown(str(desc_field or ''))
        desc = convert_jira_to_markdown(desc)
        # desc = str(desc_field)
        # "{'type': 'doc', 'version': 1, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Once steps in '}, {'type': 'inlineCard', 'attrs': {'url': 'https://luminorgroupcloud.atlassian.net/browse/CB-4817'}}, {'type': 'text', 'text': ' '}, {'type': 'hardBreak'}, {'type': 'text', 'text': 'are done, we have to connect to Data Mesh Kafka'}, {'type': 'hardBreak'}, {'type': 'hardBreak'}, {'type': 'text', 'text': 'Tasks'}]}, {'type': 'bulletList', 'content': [{'type': 'listItem', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Create topics in Data mesh Kafka'}]}]}, {'type': 'listItem', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Create access to Data Mesh Kafka'}]}]}, {'type': 'listItem', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Add Kafka connection to Oracle conector'}]}]}]}]}"


        stories.append({
            'name': issue.get('key'),
            'url': jira_server + '/browse/' + issue.get('key'),
            'summary': issue.get('fields', {}).get('summary'),
            'status': "`" + issue.get('fields', {}).get('status', {}).get('name') + "` ",
            # 'assignee': issue.get('fields', {}).get('assignee', {}).get('displayName'),
            # 'reporter': issue.get('fields', {}).get('reporter', {}).get('displayName'),
            # 'priority': issue.fields.priority.name if issue.fields.priority else None,
            'description': desc,
            # 'created': issue.fields.created,
            # 'updated': issue.fields.updated,
            # 'labels': issue.fields.labels,
        })

    return stories
