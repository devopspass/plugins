action = "docker_start_container"
doc = {
    "metadata": {
        "actions":[
            {
                "object_types": "application",
                "application_name": "Docker",
                "title": "Generate Dockerfile",
                "description": "Generate Dockerfile for your application. Featured by Quân Huỳnh - https://github.com/hoalongnatsu/Dockerfile\n",
                "icon": "fab fa-docker",
                "playbook": "plugins/docker/playbooks/generate_dockerfile.yml",
                "required_options": {
                    "folder_name":{
                        "type": "folder",
                        "title": "Your project home folder",
                        "remember":True,
                        "remember_key":"name"
                    },
                    "app_type": {
                        "type": "dropdown",
                        "default":"Python\nPython Django\nPython Flask\nGolang\nJava Spring Boot\nJava Quarkus\nNodeJS\nNodeJS node-gyp\nNodeJS NestJS\nReact\nReact pnpm\nASP.NET Core\nASP.NET Core Alpine\nRuby RoR\nRuby RoR with assets\nRust root\nRust non-priviledged\nDart\nR Studio MSSQL\nR Studio MySQL\n",
                        "title": "For which language you want to generate Dockerfile",
                        "remember":True,
                        "remember_key":"name"
                    }
                },
                "by_user": True,
                "action": "generate_dockerfile",
                "doc_type": "application"
            },
            {
                "object_types": "application",
                "application_name": "Docker",
                "title": "Start Docker container",
                "description": "Start Docker container from image\n",
                "icon": "fas fa-play",
                "command": "plugins/docker/scripts/docker_start_container.py",
                "required_settings": [
                    "docker.command"
                ],
                "required_options": {
                    "name": {
                        "type":"string",
                        "title":"Name",
                        "remember":True,
                        "remember_key":"name",
                        "default":"",
                        "value":"autok3s"
                    },
                    "image":{
                        "type":"string",
                        "default":"ubuntu:focal",
                        "title":"Image",
                        "remember":True,
                        "remember_key":"name",
                        "value":"cnrancher/autok3s:v0.9.2"
                    },
                    "start_as":{
                        "type":"dropdown",
                        "title":"Start as",
                        "default":"Interactive|-it\nDaemon/Detached|-d\n",
                        "remember":True,
                        "remember_key":"name",
                        "value":"-d"
                    },
                    "command":{
                        "type":"string",
                        "title":"Command",
                        "remember":True,
                        "remember_key":"name",
                        "default":"",
                        "value":""
                    },
                    "volumes":{
                        "type":"string",
                        "title":"Volumes",
                        "description":"Command separated volumes - `/home/user/.aws/:/root/.aws/,/home/user/.kitchen:/root/.kitchen`",
                        "remember":True,
                        "remember_key":"name",
                        "default":"",
                        "value":"/var/run/docker.sock:/var/run/docker.sock"
                    },
                    "ports":{
                        "type":"string",
                        "title":"Expose ports",
                        "description":"Command separated ports to expose - `80,8080`",
                        "remember":True,
                        "remember_key":"name",
                        "default":"",
                        "value":""
                    },
                    "network":{
                        "type":"dropdown",
                        "title":"Network Type",
                        "default":"bridge\nnone\nhost\ncontainer:(specify below)\nnetwork (specify below)\n",
                        "value":"host"
                    },
                    "network_container":{
                        "type":"string",
                        "title":"Network \"container:\" or \"network\"",
                        "description":"If Network Type **container** or *network* used",
                        "remember":True,
                        "remember_key":"name",
                        "default":"",
                        "value":""
                    }
                },
                "by_user":True,
                "action":"docker_start_container",
                "doc_type":"application"
            }
        ],
        "description":"Platform for developing, shipping, and running applications in containers.",
        "description_long":"Docker is a platform for developing, shipping, and running applications in containers, enabling consistent and scalable software delivery.",
        "disabled":False,
        "docs":[
            {
                "doc_type":"docker_container",
                "title":"Docker containers",
                "filter_field":"name"
            },
            {
                "doc_type":"docker_images",
                "title":"Docker images",
                "filter_field":"name"
            }
        ],
        "favourite":False,
        "icon":"assets/icons/apps/docker.png",
        "idx":2,
        "name":"Docker",
        "recommended":True,
        "doc_type":"application"
    },
    "id": "0"
}

import requests
import urllib.parse
import json, os
import webbrowser

response = requests.request("GET", f"http://127.0.0.1:10818/action?action={action}&doc={urllib.parse.quote_plus(json.dumps(doc))}")

res = json.loads(response.content)
if res['exitcode'] == 0:
    print("Opening K8s endpoint...")
    webbrowser.open_new_tab('http://127.0.0.1:8080/')
else:
    print("Something went wrong...")
    print(res.get('stdout'))
    print(res.get('stderr'))
    exit(1)