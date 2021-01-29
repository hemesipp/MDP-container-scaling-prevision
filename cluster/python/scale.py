from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import config

config.load_kube_config()


# Enter a context with an instance of the API kubernetes.client
api_instance = kubernetes.client.AppsV1Api()
name = 'consumer-deployment' # str | name of the Scale
namespace = 'default' # str | object name and auth scope, such as for teams and projects
body = {"spec": {"replicas": 3}} # object |

api_response = api_instance.patch_namespaced_deployment_scale(name, namespace, body)
pprint(api_response)