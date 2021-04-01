from fastapi import FastAPI
import uvicorn
from random import *
from kubernetes import client, config
import os
import kafka
import time


def new_consumer():
    try:
        consumer = kafka.KafkaConsumer('topic_1',
                                       bootstrap_servers='broker:9092',
                                       group_id='mygroup',
                                       auto_offset_reset='earliest',
                                       consumer_timeout_ms=10000)
    except kafka.errors.NoBrokersAvailable:
        time.sleep(30)
        consumer = new_consumer()

    return consumer


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
consumer = new_consumer()
output_offset = 0
input_offset = 0


@app.get("/work/{name}")  # id of consumer in entry
def job_handler(name: str):
    global act_cons_list
    global nb_cons_wanted
    global last_cons_id
    global consumer
    global output_offset
    r = random()
    if r < 0.1:
        nb_cons_wanted = randint(1, 10)
    if nb_cons_wanted < len(act_cons_list):
        real_name = name.rstrip('\n')
        i = act_cons_list.index(int(real_name[13:]))
        del act_cons_list[i]
        os.system("python3 remove_new_consumer.py " + real_name)
        return "Die"
    else:
        while nb_cons_wanted > len(act_cons_list):
            last_cons_id += 1
            act_cons_list.append(last_cons_id)
            os.system("python3 create_pod.py " + str(last_cons_id))
        consumer.resume()
        record = consumer.poll(max_records=1)
        topic, value = list(record.items())[0]
        consumer.commit()
        consumer.pause()
        output_offset = int(value[0][2]) + 1
        return {"message": value[0][6]}


@app.get("/metrics/{offset}")
def get_metrics(offset: int):
    global input_offset
    input_offset = offset


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
    global act_cons_list
    global nb_cons_wanted
    global last_cons_id
    while True:
        time.sleep(5)
        print("-----METRICS-----")
        nb_pod = len(act_cons_list)
        nb_waiting_work = input_offset - output_offset
        ratio = nb_waiting_work / nb_pod
        #nb_cons_wanted = abs(nb_cons_wanted * ratio)
        print("NB POD: " + str(nb_pod))
        print("NB WAITING WORK: " + str(nb_waiting_work))
        print("RATIO: " + str(ratio))
        print("NB CONSUMER WANTED: " + str(nb_cons_wanted))
