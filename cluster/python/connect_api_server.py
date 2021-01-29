from kubernetes import client, config, watchdef main():
    config.load_kube_config()