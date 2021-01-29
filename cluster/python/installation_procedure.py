from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
import os
import utils

conf = utils.load_auto_config(os.getenv('KUBECONFIG'))
client = utils.setup_requests(conf)

ret = client.get(f('{conf.url}/api/v1/namespaces'))
assert ret.status_code == 200

"""
# Enter a context with an instance of the API kubernetes.client
with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kubernetes.client.AdmissionregistrationApi(api_client)
    
try:
        api_response = api_instance.get_api_group()
        pprint(api_response)
except ApiException as e:
        print("Exception when calling AdmissionregistrationApi->get_api_group: %s\n" % e)
"""

for i in ret.json()['items']:
    print(i['metadata']['name'])