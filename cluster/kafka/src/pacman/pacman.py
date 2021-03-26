from fastapi import FastAPI
import uvicorn
from random import *
from kubernetes import client, config
import os

# import time

def remove_pod(name):
    config.load_incluster_config()

    api_instance = client.CoreV1Api()

    namespace = 'default'  # str

    return api_instance.delete_namespaced_pod(name, namespace)


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


app = FastAPI()

act_cons_list = [1]
nb_cons_wanted = 4
last_cons_id = 1


@app.get("/{name}")  # id of consumer in entry
def job_handler(name: str):
    global act_cons_list
    global nb_cons_wanted
    global last_cons_id
    r = random()
    if r < 0.1:
        nb_cons_wanted = randint(1, 10)
    if nb_cons_wanted < len(act_cons_list):
        real_name = name.rstrip('\n')
        i = act_cons_list.index(int(real_name[13:]))
        del act_cons_list[i]
        os.system("python3 remove_new_consumer.py " + real_name)
        return "Die"
        #ret_val = await remove_pod(real_name)
        #return ret_val
    else:
        while nb_cons_wanted > len(act_cons_list):
            last_cons_id += 1
            act_cons_list.append(last_cons_id)
            os.system("python3 create_pod.py " + str(last_cons_id))
        return {"message": "first_job_id"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
