#!/Users/Aleksey_Hariton1/.devopspass-ai/mamba/envs/codex/bin/python
#
# ls -1 */actions.yaml | while read a; do ./readme-gen.py $a > `dirname $a`/README.md; done
import sys
import yaml

def generate_markdown(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    markdown_lines = []
    applications = {}

    for key, value in data.items():
        app_name = value.get('application_name', '')
        if app_name == '':
            app_name = value.get('object_types', '')
        if app_name not in applications:
            applications[app_name] = []

        action_title = value.get('title', 'No Title')
        action_description = value.get('description', 'No Description')
        applications[app_name].append({
            'title': action_title,
            'description': action_description,
            'key': key
        })

    for app_name, actions in applications.items():
        markdown_lines.append(f"# {app_name}\n")
        for action in actions:
            markdown_lines.append(f"**{action['title']}**\n")
            markdown_lines.append(f"{action['description']}\n")
            markdown_lines.append("\n")

    return "\n".join(markdown_lines)

# Example usage
yaml_file = sys.argv[1]
markdown_doc = generate_markdown(yaml_file)
print(markdown_doc)

