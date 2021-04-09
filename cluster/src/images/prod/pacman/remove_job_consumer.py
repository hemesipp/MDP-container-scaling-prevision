from kubernetes import client, config
import sys


def remove_pod(name):
    config.load_incluster_config()

    api_instance = client.CoreV1Api()

    namespace = 'default'  # str
    return api_instance.delete_namespaced_pod(name, namespace)


if __name__ == "__main__":
    remove_pod(sys.argv[1:][0])
