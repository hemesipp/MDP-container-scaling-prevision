from kubernetes import client, config

"""
config.load_kube_config()

api_instance = client.CoreV1Api()

namespace = 'default'  # str
name = 'new-consumer'  # str | Pod name, e.g. via api_instance.list_namespaced_pod(namespace)

api_response = api_instance.delete_namespaced_pod(name, namespace)
print(api_response)
"""


def remove_pod(id):
    config.load_kube_config()

    api_instance = client.CoreV1Api()

    namespace = 'default'  # str
    name = 'new-consumer' + id  # str | Pod name, e.g. via api_instance.list_namespaced_pod(namespace)

    return api_instance.delete_namespaced_pod(name, namespace)
