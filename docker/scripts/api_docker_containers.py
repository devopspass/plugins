import docker

def get_icon(image_name):
    icon_mapping = {
        "postgres":"apps/postgresql.png",
        "mysql":"apps/mysql.png",
        "ruby":"apps/ruby.png",
        "golang":"apps/golang.png",
        "php":"apps/php.png",
        "aix": "os/aix.png",
        "alpine": "os/alpine.png",
        "centos": "os/centos.png",
        "debian": "os/debian.png",
        "fedora": "os/fedora.png",
        "freebsd": "os/freebsd.png",
        "hp-ux": "os/hp-ux.png",
        "linux": "os/linux.png",
        "macos": "os/macos.png",
        "opensuse": "os/opensuse.png",
        "oracle": "os/oracle.png",
        "redhat": "os/redhat.png",
        "solaris": "os/solaris.png",
        "ubuntu": "os/ubuntu.png",
        "windows": "windows.png",
        "ansible": "apps/ansible.png",
        "appdynamics": "apps/appdynamics.png",
        "argocd": "apps/argocd.png",
        "artifactory": "apps/artifactory.png",
        "aws": "apps/aws.png",
        "azure": "apps/azure.png",
        "bamboo": "apps/bamboo.png",
        "beyondtrust": "apps/beyondtrust.png",
        "bitbucket": "apps/bitbucket.png",
        "chef": "apps/chef.png",
        "circleci": "apps/circleci.png",
        "conda": "apps/conda.png",
        "confluence": "apps/confluence.png",
        "cyberark": "apps/cyberark.png",
        "datadog": "apps/datadog.png",
        "elasticsearch": "apps/elasticsearch.png",
        "elk": "apps/elastic-stack.png",
        "fluentd": "apps/fluentd.png",
        "gatling": "apps/gatling.png",
        "gitlab": "apps/gitlab.png",
        "git": "apps/git.png",
        "grafana": "apps/grafana.png",
        "gremlin": "apps/gremlin.png",
        "hadoop": "apps/hadoop.png",
        "helm": "apps/helm.png",
        "honeycomb": "apps/honeycomb.png",
        "java": "apps/java.png",
        "temurin": "apps/java.png",
        "openjdk": "apps/java.png",
        "jenkins": "apps/jenkins.png",
        "lightstep": "apps/lightstep.png",
        "loggly": "apps/loggly.png",
        "logz": "apps/logz-io.png",
        "mimir": "apps/mimir.png",
        "nagios": "apps/nagios.png",
        "newrelic": "apps/newrelic.png",
        "nexus": "apps/nexus.png",
        "node": "apps/nodejs.png",
        "nomad": "apps/nomad.png",
        "observe": "apps/observe.png",
        "octopus": "apps/octopus.png",
        "okta": "apps/okta.png",
        "openshift": "apps/openshift.png",
        "opentelemetry": "apps/open-telemetry.png",
        "packer": "apps/packer.png",
        "pagerduty": "apps/pagerduty.png",
        "pingdom": "apps/pingdom.png",
        "powershell": "apps/powershell.png",
        "prometheus": "apps/prometheus.png",
        "pulumi": "apps/pulumi.png",
        "puppet": "apps/puppet.png",
        "python": "apps/python.png",
        "rancher": "apps/rancher.png",
        "raygun": "apps/raygun.png",
        "rkt": "apps/rkt.png",
        "rundeck": "apps/rundeck.png",
        "saltstack": "apps/saltstack.png",
        "scalyr": "apps/scalyr.png",
        "sentry": "apps/sentry.png",
        "servicenow": "apps/servicenow.png",
        "shiftleft": "apps/shiftleft.png",
        "slack": "apps/slack.png",
        "snyk": "apps/snyk.png",
        "sonarqube": "apps/sonarqube.png",
        "spinnaker": "apps/spinnaker.png",
        "splunk": "apps/splunk.png",
        "spot-io": "apps/spot-io.png",
        "sumologic": "apps/sumologic.png",
        "systemd": "apps/systemd.png",
        "teamcity": "apps/teamcity.png",
        "tehama.png": "tehama.png",
        "tenable": "apps/tenable.png",
        "terraform": "apps/terraform.png",
        "thanos": "apps/thanos.png",
        "travis": "apps/travis.png",
        "trello": "apps/trello.png",
        "vault": "apps/vault.png",
        "victoria-metrics": "apps/victoria-metrics.png",
        "wavefront": "apps/wavefront.png",
        "workday": "apps/workday.png",
        "wrike": "apps/wrike.png",
        "zabbix": "apps/zabbix.png",
        "zenoss": "apps/zenoss.png",
        "zoom": "apps/zoom.png",
    }

    # Extract the base image name from the full image name
    base_image_name = image_name.split("/")[-1].split(":")[0]

    matching_keys = [key for key in icon_mapping.keys() if key in base_image_name]

    # Use the mapping, or default to "unknown.png" if not found
    return icon_mapping.get(matching_keys[0], None) if matching_keys else 'apps/docker.png'



def list():
    """
    List information about running Docker containers.

    Returns:
    - list: List of dictionaries containing container information.
    """
    client = docker.from_env()

    try:
        # Get a list of running containers
        containers = client.containers.list()

        # Process container information
        containers_info = []
        for container in containers:
            nets = sorted(container.attrs['NetworkSettings']['Networks'].keys())
            m = []
            for mount in container.attrs['Mounts']:
                rw = 'ro'
                if mount['RW']:
                    rw = 'rw'
                m.append(f"{mount['Source']}:{mount['Destination']} ({mount['Type']},{rw})")
            container_info = {
                'icon': f"assets/icons/{get_icon(container.image.tags[0])}",
                'name': str(container.name),
                'id': str(container.short_id),
                'image': str(container.image.tags[0]),
                'command': ' '.join(container.attrs['Config']['Cmd']),
                'status': str(container.status),
                'ports': str(container.attrs['HostConfig']['PortBindings']),
                'volumes': '<br/>'.join(m),
                'network_type': ' '.join(nets),
                # 'is_privileged': container.attrs['HostConfig']['Privileged']
            }
            containers_info.append(container_info)

        return containers_info

    except docker.errors.APIError as e:
        print(f"Error: {e}")
        return None
