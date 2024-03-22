import os
import yaml
import dns.resolver
from urllib.parse import urlparse
from kubernetes import config as kubeconfig

import cdx

class KubernetesProviderDetector:
    def __init__(self, kubeconfig_path="~/.kube/config"):
        self.kubeconfig_path = os.path.expanduser(kubeconfig_path)
        self.k8s_providers = {}

    def extract_host_from_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.hostname:
            return parsed_url.hostname
        return None

    def get_cname_records(self, host):
        try:
            cname_records = dns.resolver.query(host, 'CNAME')
            return [str(record.target) for record in cname_records]
        except dns.resolver.NoAnswer:
            return []

    def determine_k8s_provider(self):
        if not os.path.isfile(self.kubeconfig_path):
            return "Unknown"

        try:
            with open(self.kubeconfig_path, "r") as config_file:
                kubeconfig = yaml.safe_load(config_file)
            contexts = kubeconfig.get("contexts", [])

            for context in contexts:
                cluster_name = context["context"]["cluster"]
                cluster_endpoint = None

                for cluster in kubeconfig.get("clusters", []):
                    if cluster["name"] == cluster_name:
                        cluster_endpoint = cluster["cluster"]["server"]
                        break

                if cluster_endpoint:
                    host = self.extract_host_from_url(cluster_endpoint)

                    if host:
                        # cname_records = self.get_cname_records(host)
                        cname_records = [host]

                        tp = 'k8s'
                        title = 'Unknown K8s provider'

                        if any("amazonaws.com" in cname for cname in cname_records):
                            tp = 'eks'
                            title = "Amazon EKS"
                        elif any("azure.com" in cname for cname in cname_records):
                            tp = 'aks'
                            title = "Azure AKS"
                        elif any("googleusercontent.com" in cname for cname in cname_records):
                            tp = 'gke'
                            title = "Google GKE"
                        elif any("openshift" in cname for cname in cname_records):
                            tp = 'ose'
                            title = "OpenShift"
                        elif any("ose" in cname for cname in cname_records):
                            tp = 'ose'
                            title = "OpenShift"
                        elif any("k3s" in cname for cname in cname_records):
                            tp = 'k3s'
                            title = "K3s"
                        elif any("k3d" in cname for cname in cname_records):
                            tp = 'k3s'
                            title = "K3s"

                        if 'k3d' in cluster["name"] or 'k3s' in cluster["name"]:
                            tp = 'k3s'
                            title = "K3s"

                        self.k8s_providers[context["name"]] = {}
                        self.k8s_providers[context["name"]]['type'] = tp
                        self.k8s_providers[context["name"]]['title'] = title
                        # Add more provider checks as needed

        except (KeyError, TypeError):
            pass

    def get_results(self):
        return self.k8s_providers

def list():
    provider_detector = KubernetesProviderDetector()
    provider_detector.determine_k8s_provider()
    k8s_providers = provider_detector.get_results()
    k8s = []

    if kubeconfig.exists(os.path.expanduser(kubeconfig.KUBE_CONFIG_DEFAULT_LOCATION)):
        contexts = kubeconfig.list_kube_config_contexts()

        d_name = contexts[1].get('name')
        for c in contexts[0]:
            name = c.get('name', '')
            k8s.append({
                'name': name,
                'icon': f"assets/icons/k8s/{k8s_providers.get(name, {}).get('type')}.png",
                'type_title': k8s_providers.get(name, {}).get('title'),
                'active': d_name == name,
            })
        k8s = sorted(k8s, key=lambda c: c['name'])
    return k8s