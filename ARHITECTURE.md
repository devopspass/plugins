## High level architecture

![High Level Architecture](https://raw.githubusercontent.com/devopspass/plugins/main/images/high-level-arch.png)

DevOps Pass AI as application consists from three parts:
* **Electron-based UI**, which is responsible for user interface and Data Sources (see below)
* **Backend** (Codex), which is written in Python
* **Plugins**, which contains main functionality of DOP

Plugins contains configuration for applications, documents, settings, actions scripts, playbooks, configuration for data sources.

On the picture below you can see how all this elements reflects in UI:

![UI elements](https://raw.githubusercontent.com/devopspass/plugins/main/images/ui-elements.png)

* **Applications**, high level entity for DOP, by adding applications you adding new actions, document types and settings.
* **Applications Links**, set of links divided by sections, which contains links to necessary resources: documentation, tools, etc.
* **Application Actions**, actions which can be run agains application, usually its tools installation, retreiving configuration, etc. Application actions could be Python script or Ansible playbook.
* **Application doc_type's**, types of documents which can be retreived for application. Each application can has many doc_type's.
* **Documents**, basic entities, which are retrieved from applications, i.e. repositories, packages, namespaces, application versions, etc. Agains documents, you can run actions.
* **Document's actions**, actions you can run against documents, like install, remove, make default, etc.
* **Settings**, settings for specific application, like URL to entry URL, terminal command, default region, etc.
* **Data Sources**, pieces of configuration which allowing retrieve information from web-applications, which can be used later in scripts. For example cookies, objects from web page, registration tokens, etc. This functionality allowing you to write scripts for web applications, which not providing common API, by simulating same HTTP requests that browser do.

## UI

UI is Electron based application written with Angular and Bootstrap.
Its allowing you to auth, pull plugins and make manipulations with applications, docs and data sources.

This piece is shipped together with DevOps Pass AI packages.

## Codex

Codex, is a backed for DevOps Pass AI, written in Python and providing interface between UI and plugins, implementing some very basic operations, leaving functionality extension to plugins.

This piece is shipped together with DevOps Pass AI packages.

## Plugins

Plugins, main functionality source. Its keeping all possible configurations for applications, including actions,settings, documents and data sources. If you want to implement some FUNCTIONALITY, you probably have to write a plugin.

All plugins are stored in GitHub repo - https://github.com/devopspass/plugins/. It is under BSD license, which means you can copy/fork/change it without any limitations.

After startup DOP pulling latest version of that repo to `~/.devopspass-ai/plugins/` folder.

If you want to make plugins for your private applications, which cannot be shared with comminity, you can clone this repo in your private repository and change plugins source in settings. After restart DOP will use your private repo instead of public one.

## Authentication and Security

DevOps Pass AI trying to keep onboarding as simple as possible, so only thing you need to login DOP is provide your email address and click link you'll receive in email.

If you're using corporate email and your organization using Enterprise subscription, DOP will pull settings, specific for your organization (plugins source, configration for various DevOps applications used in your org, etc).

We're trying to keep everything as much simple as possible, so security questions should be convered by specific applications. Means, user MAY have URL to your JIRA, but if he can get ACCESS to it or not, should not be controlled by DOP. If user stores access_token for Confluence on his local, DOP should not control if he CAN access with that token Confluence, it should be controlled on AD/Confluence level, etc.

If you want your plugins to be private, put it on Git-server behind VPN. Again, DOP should not be responsible for your privacy, its giving user some simplification and automation for routine DevOps activities, but keep in mind that user can do the same without DOP.

## Applications

High level entity for DevOps Pass, if user want to add some piece of functionality to DOP or interact with some DevOps tool, he have to add application.

List of all available applications stored in `~/.devopspass-ai/plugins/apps.yaml`
This YAML stores arrays of applications, with it descriptions and set of links.

**Example for Git:**

```yaml
- name: Git
  icon: assets/icons/apps/git.png
  description: Git is a distributed version control system designed for tracking changes ...
  description_long: Git is a powerful distributed version control system widely used...
  recommended: true
  sections:
  - name: Git
    urls:
    - name: Downloads
      url: https://git-scm.com/downloads
    - name: "'Pro Git' book"
      url: https://git-scm.com/book/en/v2
    - name: GitFlow
      url: https://datasift.github.io/gitflow/IntroducingGitFlow.html
    - name: Semantic versioning
      url: https://semver.org/
```

Application definition contains name, URL to icon, description (long), whether that app should appear in recommended apps or not and list of links for app. In git case there is one section "Git" contains links to some documentation, books and useful links.

Applications from `apps.yaml` later could be added by user in UI:

![Add application](https://raw.githubusercontent.com/devopspass/plugins/main/images/add-application.png)

After adding application by user, it will be added to user's defined applications, stored in `~/.devopspass-ai/applications.yml`. Later on user can do any changes to application, like change URL's, sections, etc.


## Application actions

Application actions, its actions which running agains application, usually its tools installation (install `kubectl`, install Terraform, etc.) or pulling data from applications (see **Data Sources**).

Application actions could be Python scripts or Ansible playbooks.
If you want to add application action, create folder with app name in `plugins/APP_NAME/` (its recommended to keep it lower case) and add `actions.yaml` file with actions definition.


### Playbook actions

Below you can find example of **Install Terraform** action:

```yaml
terraform_install:
  object_types: application
  application_name: Terraform
  title: Install Terraform
  description: |
    Install Terraform on your local. Versions list can be found here - https://releases.hashicorp.com/terraform/, **latest** version will install latest stable version of Terraform
  icon: fas fa-download
  playbook: plugins/terraform/playbooks/install.yml
  required_options:
    req_terraform_version:
      title: Terraform version to Install
      remember: true
      remember_key: name
      type: string
      default: latest
```

Please note, that comparing to other icon's in DOP, actions icons are FontAwesome 5 icon id - https://fontawesome.com/v5/search?q=&o=r&m=free
You can see how it reflects in UI.

![Application action](https://raw.githubusercontent.com/devopspass/plugins/main/images/application-action.png)


Also in addition to command you can specify list of settings, which have to be passed to command/playbook.

```yaml
  required_settings:
    - terminal.command
```


Each option or setting will be passed to playbook as variables:

Example of playbook:

```yaml
---
- name: Install Terraform
  hosts: localhost
  connection: local
  vars:
    arch_mapping:  # Map ansible architecture {{ ansible_architecture }} names to Docker's architecture names
      x86_64: amd64
      aarch64: arm64
  tasks:
    - name: Base tasks
      ansible.builtin.include_tasks:
        file: "../../_common/playbooks/base.yml"

   # ...

    - name: Set version
      ansible.builtin.set_fact:
        terraform_version: "{{ (req_terraform_version == 'latest') | ternary(latest_terraform_version, req_terraform_version)}}"
```

Settings will pass in the same way, but dots in names will be replaces with underscores.

There is some Ansible variables always passed to Ansible Playbook running from DOP:

| Ansible var | Value |
|-------------|-------|
| dop_home_path | `~/.devopspass-ai/` |
| user_home_path | `~/` |
| codex_root_path | Path where Codex is running `main.py` |
| codex_env_path | `~/.devopspass-ai/mamba/envs/codex/` |
| python_bin_path | Python binary path |
| mamba_bin_path | Path to mamba binary - `~/.devopspass-ai/mamba` |
| git_bin_path | Path to `git` or `git.exe` binary |
| settings_file_path | `~/.devopspass-ai/settings.yaml` |
| settings_org_file_path | `~/.devopspass-ai/settings-org.yaml` |
| applications_file_path | `~/.devopspass-ai/applications.yaml` |
| applications_org_file_path | `~/.devopspass-ai/applications-org.yaml` |
| plugins_path | `~/.devopspass-ai/plugins/` |
| all_applications_file_path | `~/.devopspass-ai/plugins/apps.yaml` |


Please note that it's mandatory to add `base` tasks at the begginning of playbook and use `local` connection in all playbooks.

```yaml
- name: Install Terraform
  hosts: localhost
  connection: local # mandatory
  tasks:
    - name: Base tasks # mandatory
      ansible.builtin.include_tasks:
        file: "../../_common/playbooks/base.yml"
   # ...
```

### Script actions

Instead of `playbook` you could specify `command`, path to Python script to run on action.

```yaml
  # ...
  required_settings:
    - terminal.command
  command: plugins/kubernetes/actions/open_in_k9s.py
```

Path to command is relative from DOP home `~/.devopspass-ai/`, please note it.

In script you can get values, settings and doc:

```python
import cdx
import sys, json

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

# ... main code
```

## Application doc_type's and doc's

Doc types, are some docs you're pulling from application, for example list of contexts for Kubernetes or AWS profiles.

Doc types defined in `plugins/*/docs.yaml` file:

```yaml
aws_profile:
  application: AWS
  title: AWS Profiles
  filter_field: name
  icon: assets/icons/apps/aws.png
  source: plugins/aws/docs/aws_profiles.py
```

* `application`, name of application doc type relates to. Please note `application` field is case sensetive and have to be the same value as application `name` in `apps.yaml`.
* `title`, tab title in UI.
* `filter_field`, filter field for documents, used on search in right pane.
* `icon`, URL to doc type icon
* `source`, Python file with `list()` method implementation

Source file should have `list()` method implemented and return list of dictionaries (documents), each document should have at least `name` field.

Field `icon` will be used to set icon URL, if not specified `doc_type` icon will be used.

Boolean field `active` can be used to add `active` label on document view:

![doc view](https://raw.githubusercontent.com/devopspass/plugins/main/images/doc-view.png)

## Documents actions

Documents actions is a key functionality item in DOP.
They are the same implementation as application actions and add in the same `actions.yaml` with the difference that `doc_type` should not be `application`, but your doc_type key:

```yaml
aws_profile_make_default:
  title: Make default
  icon: fas fa-check
  object_types: aws_profile
  command: |
    plugins/aws/actions/make_default.py
```

## Data sources

Data sources are very important part of DOP which helping to introduce automation for applications where you have no API or have no access to it.

Key idea here, pull some data from user's web browser session, like cookies, some data, application settings, etc.

Data sources describe in `plugins/*/ds.yaml` files, here is an example of Data Source for AWS Landing Zone SSO page.

```yaml
id: aws_apps
# start_url: provided from settings
description: AWS Apps creds SSO
icon: https://avatars.githubusercontent.com/u/2232217?v=4
title: AWS Apps SSO
check_script: plugins/aws/actions/check_aws_token.py
actions:
  - url_match: https://.*.awsapps.com/start/.*
    cookies:
      - name: aws_sso_token
        domain: start_url
        key: x-amz-sso_authn
    if: aws_accounts
    sleep: 2500
    name: aws_bearer_token
  - url_match: https://.*.awsapps.com/start/.*
    extract_js:
      - name: check
        js: |
          var btns = document.getElementsByTagName('button')
          var aws_accounts = []
          setTimeout(function(){
              var i = 0
              for(btn of btns){
                if(i > 9){
                  var x = btn.getElementsByTagName('strong')
                  if(x && x[0]){
                    aws_accounts.push(x[0].textContent)
                  }
                }
                i++
              }
              console.log(aws_accounts)
              return aws_accounts
          }, 2000);
  - url_match: https://.*.awsapps.com/start/.*
    if: aws_accounts
    finish: true
    sleep: 4000
    results_js: aws_accounts
```

By default, there is no way to retrieve `x-amz-sso_authn` to pull list of accounts and profiles you have access to, but you can ask user to start webbrowser session, login to this page and DOP will automatically extract necessary data and store it in user profile keychain.

Check script receives result of previous run and checks, if data from DS have to be retreived again (i.e. if token/cookie expired), if exit code is 0 then no need to start browser session again and action can use previous results. If exit code not 0, DS sequence will be started to retreive necessary data.
