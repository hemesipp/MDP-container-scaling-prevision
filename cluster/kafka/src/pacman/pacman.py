from fastapi import FastAPI
import os
import uvicorn
from random import *
#import add_new_consumer.py
#from kubernetes import client, config

# import time
"""
def remove_pod(name):
    config.load_kube_config()

    api_instance = client.CoreV1Api()

    namespace = 'default'  # str

    return api_instance.delete_namespaced_pod(name, namespace)
"""

app = FastAPI()


@app.get("/{name}")  # id of consumer in entry
def job_handler(name: str):
    act_cons_list = [1, 13, 21]
    nb_cons_wanted = 1
    last_cons_id = 23
    if nb_cons_wanted < len(act_cons_list):
        os.system("python3 remove_new_consumer.py")
    else:
        return {"message": "first_job_id"}
    """
    r = random()
    if r < 0.1:
        nb_cons_wanted = randint(1, 10)
        while nb_cons_wanted > len(act_cons_list):
            last_cons_id += 1
            add_new_consumer.create_pod(last_cons_id)
            act_cons_list.append(last_cons_id)
    # main()
    """
    return {"name": name}


"""
main est appelée à chaque nouvelle requete reçu

waiting_list: liste de new_consumer en attente
nb_container_asked: valeur rendue par l'algo de prédiction
nb_container: nombre de pods actifs
"""

"""
def main(nb_container_asked, nb_container, waiting_list):
    while True:
        while nb_container_asked<=nb_container:
            remove_new_consumer(waiting_list[0])
            nb_container-=1
        while nb_container_asked>=nb_container:
            add_new_consumer(nb_container_asked)
            nb_container+=1
        if nb_container_asked==nb_container:
            #Send packet
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
