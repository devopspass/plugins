# DevOps Pass AI Plugins

This repo contains DevOps Pass AI plugins, which allowing you to extend basic functionality.

You can fork this repo and configure DOP for your specific case and/or organization, add plugins/actions you need.

## Application plugin example

```yaml
git_generate_config:
  title: Configure git
  description: |
    You can configure git client user name, email and merge options...
  icon: fab fa-git
  object_types: application
  application_name: Git
  playbook: plugins/git/playbooks/setup_git.yml
  required_settings:
    - user.name
    - user.email
  show_settings: true
```

## Host plugin example

```yaml
ssh_host:
  title: SSH
  icon: fas fa-terminal
  object_types: unix_host
  command: |
    plugins/_ssh/actions/ssh_host.py
  required_settings:
    - ssh.command
    - ssh.command.jumphost_options
    - actions.ssh_host
  required_options:
    ssh_user:
      type: string
      default: root
      title: SSH User Name
      remember: true
      remember_key: ip
```

## AWS Profile plugin example

```yaml
aws_open_console:
  title: Open AWS Console
  icon: fab fa-solid fa-brands fa-aws
  object_types: aws_profile
  command: |
    plugins/aws/actions/open_console.py
  required_settings:
    - actions.aws_open_console
```

## K8s Context plugin example

```yaml
k8s_set_default_context:
  title: Set Context as default
  icon: fas fa-star
  object_types: k8s_context
  command: |
    plugins/k8s/actions/set_default_context.py

```
