import docker

def error(msg: str):
    return [
            {
                'name': 'ERROR',
                'icon': 'assets/icons/general/error.png',
                'error': msg
            }
        ]

def get_icon(image_name):
    icon_mapping = {
        "gitea": "apps/gitea.png",
        "postgres":"apps/postgresql.png",
        "mysql":"apps/mysql.png",
        "mariadb":"apps/mysql.png",
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
        "argo-cd": "apps/argocd.png",
        "argo-workflows": "apps/argocd.png",
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
        "elastic-stack": "apps/elastic-stack.png",
        "logstash": "apps/elastic-stack.png",
        "kibana": "apps/elastic-stack.png",
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
        "nginx": "apps/nginx.png",
        "redis": "apps/redis.png",
        "mongo": "apps/mongodb.png",
        "mongodb": "apps/mongodb.png",
        "tomcat": "apps/tomcat.png",
        "zookeeper": "apps/zookeeper.png",
        "spark": "apps/spark.png",
        "rabbitmq": "apps/rabbitmq.png",
        "memcached": "apps/memcached.png",
        "kube-state-metrics": "apps/k8s.png",
        "kubernetes": "apps/k8s.png",
        "kafka": "apps/kafka.png",
        "etcd": "apps/etcd.png",
        "drupal": "apps/drupal.png",
        "cassandra": "apps/cassandra.png",
        "airflow": "apps/airflow.png",
        "apache": "apps/apache.png",
        "cassandra": "apps/cassandra.png",
        "cert-manager": "apps/cert-manager.png",
        "clickhouse": "apps/clickhouse.png",
        "concourse": "apps/concourse.png",
        "consul": "apps/consul.png",
        "flink": "apps/flink.png",
        "haproxy": "apps/haproxy.png",
        "influxdb": "apps/influxdb.png",
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
    try:
        client = docker.from_env()
    except:
        return error("Failed to connect to Docker, if its running?!")

    try:
        # Get a list of running containers
        containers = client.containers.list(all=True)

        # Process container information
        containers_info = []
        for container in containers:
            nets = sorted(container.attrs['NetworkSettings']['Networks'].keys())
            m = []
            for mount in container.attrs['Mounts']:
                rw = 'ro'
                if mount['RW']:
                    rw = 'rw'
                if mount['Type'] != 'volume':
                    m.append(f"{mount['Source']}:{mount['Destination']} ({mount['Type']},{rw})")

            command = container.attrs['Config']['Cmd']

            if command:
                command = ' '.join(container.attrs['Config']['Cmd'])
            else:
                command = ''
            container_info = {
                'icon': f"assets/icons/{get_icon(container.image.tags[0])}",
                'name': str(container.name),
                'id': str(container.short_id),
                'image': str(container.image.tags[0]),
                'command': command,
                'status': str(container.status),
                'ports': str(container.attrs['HostConfig']['PortBindings']),
                'volumes': '\n'.join(m),
                'network_type': ' '.join(nets),
                # 'is_privileged': container.attrs['HostConfig']['Privileged']
            }
            containers_info.append(container_info)

        return containers_info

    except docker.errors.APIError as e:
        print(f"Error: {e}")
        return None
