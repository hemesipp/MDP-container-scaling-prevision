from fastapi import FastAPI
import uvicorn
from random import *
from kubernetes import client, config

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

    container = client.V1Container(name="new-consumer-" + str(id), image="new-consumer:latest", image_pull_policy="Never")

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
    print(act_cons_list)
    print(nb_cons_wanted)
    print(last_cons_id)
    print(len(act_cons_list))
    if nb_cons_wanted < len(act_cons_list):
        real_name=name.rstrip('\n')
        i = int(real_name[-1:])
        del act_cons_list[i-1]
        return remove_pod(real_name)
    else:
        while nb_cons_wanted > len(act_cons_list):
            last_cons_id += 1
            act_cons_list.append(last_cons_id)
            create_pod(last_cons_id)
        return {"message": "first_job_id"}



"""
main est appelée à chaque nouvelle requete reçu

waiting_list: liste de new_consumer en attente
nb_container_asked: valeur rendue par l'algo de prédiction
nb_container: nombre de pods actifs
"""


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
    """
    nb_container = 0
    While True:
        #How to wait a request and add to waiting_list?
        nb_container_asked = algo(param1, param2, nb_container)         
        main(nb_container_asked, nb_container, waiting_list)
    """
