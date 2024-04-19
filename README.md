<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️--><p align="center">
  <img src="https://static.wixstatic.com/media/09a6dd_eae6b87971dd4d14ba7792cdd237dd76~mv2.png" alt="Logo" width="300" height="auto" />
</p>
<p align="center">
		<a href="https://github.com/devopspass/devopspass"><img alt="Release" src="https://img.shields.io/github/release/devopspass/devopspass.svg" height="20"/></a>
<a href=""><img alt="Downloads" src="https://img.shields.io/github/downloads/devopspass/devopspass/total" height="20"/></a>
<a href="https://medium.com/@devopspass/"><img alt="Medium" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" height="20"/></a>
<a href="https://dev.to/devopspass"><img alt="dev.to" src="https://img.shields.io/badge/dev.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" height="20"/></a>
<a href="https://www.linkedin.com/company/devopspass-ai"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" height="20"/></a>
<a href="https://www.youtube.com/@DevOpsPassAI"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" height="20"/></a>
<a href="https://twitter.com/devops_pass_ai"><img alt="Twitter" src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" height="20"/></a>
	</p>

<p align="center">
  <b>DevOps Pass AI - Keep DevOps Simple Stupid</b></br>
  <sub>Make DevOps-related activities one-click simple, without additional reading and searching.<sub>
</p>

<br />

# DevOps Pass AI Plugins

This repo contains DevOps Pass AI plugins, which allowing you to extend functionality. This repo in licensed under BSD license, so you can reuse/copy/change it without any limitations.

You can fork this repo and configure DOP for your specific case and/or organization, add plugins/actions you need.

## 📝 Documentation

For more details about types of plugins and its configuration, you can check [Architecture doc](https://github.com/devopspass/plugins/blob/main/ARHITECTURE.md).

## 💬 Join community

Join our Slack community, ask questions, contribute, get help!

[<img src="https://cloudberrydb.org/assets/images/slack_button-7610f9c51d82009ad912aded124c2d88.svg" width="150">](https://join.slack.com/t/devops-pass-ai/shared_invite/zt-2gyn62v9f-5ORKktUINe43qJx7HtKFcw)

## 🏗️ Plugins scaffolds

Of course we're trying to make plugins development simple stupid, so you can generate scaffolds for plugins using DOP itself.

Add **DevOps Pass AI** application from applications list and find actions, which can help you generate scaffolds.

![Plugins scaffolds](https://raw.githubusercontent.com/devopspass/plugins/main/images/plugins-scaffolds.png)

## 🛠️ Developing plugins

To start development of plugins you have to make a fork of that repo and set in DOP settings that you want to pull plugins from another repo:

![Plugins source settings](https://raw.githubusercontent.com/devopspass/plugins/main/images/plugins-source.png)

After that restart DOP and open `~/.devopspass-ai/plugins` in your editor.

When you do changes in configuration files (`apps.yaml`, `actions.yaml`, `docs.yaml`, `ds.yaml`) you have to force DOP to reload plugins from file system, click on your avatar in top right and click **Reload plugins** and wait for a few seconds to get changes applied. In some cases you also have to change application (when you changing doc actions).

For scripts and playbooks changes there is no need to reload plugins and you can use **Retry** button in action window.

You also may need to see Codex logs, when debuging your code, for example if youre doing `print()` in doc script, you can find output, by clicking on your avatar (top right) and clicking **Codex console**.

Once you're done with changes, push your changes to Git and send us PR ;)
