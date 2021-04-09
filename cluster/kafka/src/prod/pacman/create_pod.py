import sys
from kubernetes import client, config

def create_pod(id):
    config.load_incluster_config()

    v1 = client.CoreV1Api()

    pod = client.V1Pod()
    pod.metadata = client.V1ObjectMeta(name="new-consumer-" + str(id))

    container = client.V1Container(name="new-consumer-" + str(id), image="new-consumer:latest",
                                   image_pull_policy="Never")

    spec = client.V1PodSpec(containers=[container], restart_policy="Always")
    pod.spec = spec

    return v1.create_namespaced_pod(namespace="default", body=pod)

if __name__ == "__main__":
    create_pod(sys.argv[1:][0])

