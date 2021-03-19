from kubernetes import client, config
from kubernetes.client.models import V1Pod, V1ObjectMeta, V1Container, V1PodSpec


def create_pod(id):
    config.load_kube_config()

    v1 = client.CoreV1Api()

    pod = client.V1Pod()
    pod.metadata = client.V1ObjectMeta(name="new-consumer" + id)

    container = client.V1Container(name="new-consumer" + id, image="new-consumer:latest", image_pull_policy="Never")

    spec = client.V1PodSpec(containers=[container], restart_policy="Always")
    pod.spec = spec

    v1.create_namespaced_pod(namespace="default", body=pod)
    print("Pod deployed.")


if __name__ == "__main__":
    create_pod("1")
