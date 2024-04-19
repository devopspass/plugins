## High level architecture

![High Level Architecture](https://raw.githubusercontent.com/devopspass/plugins/main/images/high-level-arch.png)

DevOps Pass AI as application consists from three parts:
* **Electron-based UI**, which is responsible for user interface and Data Sources (see below)
* **Backend** (Codex), which is written in Python
* **Plugins**, which contains main functionality of DOP

Plugins contains configuration for applications, documents, settings, actions scripts, playbooks, configuration for data sources.

On the picture below you can see how all this elements reflects in UI:

![UI elements](https://raw.githubusercontent.com/devopspass/plugins/main/images/ui-elements.png)

