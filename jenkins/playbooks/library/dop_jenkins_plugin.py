import time
import traceback
from ansible.module_utils.basic import AnsibleModule
import requests

def get_jenkins_crumb(url, username, password):
    auth = (username, password)
    response = requests.get(url, auth=auth)
    crumb = response.json().get('crumb')
    return crumb

def install_plugins(url, username, password, crumb, plugins):
    data = {
        'dynamicLoad': '',
        'Jenkins-Crumb': crumb,
        'json': '{"Jenkins-Crumb":"' + crumb + '"}'
    }
    for plugin in plugins:
        data[f'plugin.{plugin}.default'] = 'on'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Jenkins-Crumb': crumb
    }
    response = requests.post(url, auth=(username, password), headers=headers, data=data, verify=False)
    return response.text

def main():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        url=dict(type='str', required=True),
        plugins=dict(type='list', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    username = module.params['username']
    password = module.params['password']
    url = module.params['url']
    plugins = module.params['plugins']

    try:
        crumb_url = f"{url}/crumbIssuer/api/json"
        crumb = get_jenkins_crumb(crumb_url, username, password)
        response = install_plugins(f"{url}/manage/pluginManager/install", username, password, crumb, plugins)

        i = 300
        while True:
            resp = requests.get(f"{url}/manage/pluginManager/updates/", auth=(username, password), verify=False)
            if not 'Pending' in resp.text:
                break
            else:
                time.sleep(1)
            i = i - 1
            if i == 0:
                module.fail_json(msg='Timeout waiting for plugins to install - 5 min, mb its finished, please check Jenkins')

        module.exit_json(changed=True, response=response)
    except Exception as e:
        module.fail_json(msg=traceback.format_exc())

if __name__ == '__main__':
    main()
