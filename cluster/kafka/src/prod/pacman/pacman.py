"""
Pacman is the gateway between  the kafka queue and the pods which are treating the processes ask by the user
It contains a fast api entity which communicate in http with the pods
The pods send GET request when they have finished to run the jobs that they received from pacman

Pacman is seen as a consumer by the kafka queue
Pacman is seen as a producer by the pods

Pacman is the one who scale the pods too. He uses the python API for kubernetes to create and delete pods.
"""

#######################################################################################################################

"""Fast Api library"""
from fastapi import FastAPI
import uvicorn

"""Python API for kubernetes"""
from kubernetes import client, config

"""Kafka library"""
import kafka

"""Other library used"""
import os
import time

"""Use for test"""
# from random import *

#######################################################################################################################

"""
Kafka consumer object : It consume messages from the kafka queue
the arguments are: the read topic, the access to the broker, the group id, the offset reset and the consumer timeout
"""


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


#######################################################################################################################


"""
Initialisation:

Creation of 'app' : Fast Api entity

Creation of global variables:
act_cons_list:
nb_cons_wanted:
last_cons_id:
kafka_consumer:
output_offset:  
input_offset:
"""

app = FastAPI()

act_cons_list = [1]
nb_cons_wanted = 4
last_cons_id = 1
kafka_consumer = new_consumer()
output_offset = 0
input_offset = 0

"""Definition of the answer to http request GET /work/{name}"""


@app.get("/work/{name}")  # id of consumer in entry
def job_handler(name: str):
    global act_cons_list
    global last_cons_id
    global kafka_consumer
    global output_offset
    """
    # Only for test
    r = random()
    if r < 0.1:
        nb_cons_wanted = randint(1, 10)
    """
    real_name = name.rstrip('\n')  # The string received from the http request as the format name\n

    if int(real_name[13:]) in act_cons_list:  # Ensures to not treat the dying pods
        if nb_cons_wanted < len(act_cons_list):  # Case where the pod requesting has to die
            i = act_cons_list.index(int(real_name[13:]))
            del act_cons_list[i]
            os.system("python3 remove_new_consumer.py " + real_name)  # Run the python code killing a pod
            return "Die"
        else:  # Case where pacman has to send new job to the requesting pod
            while nb_cons_wanted > len(act_cons_list):  # Case where pacman has to create pods
                last_cons_id += 1
                act_cons_list.append(last_cons_id)
                os.system("python3 create_pod.py " + str(last_cons_id))  # Run the python code creating pod
            kafka_consumer.resume()  # Wake up the kafka consumer entity
            record = kafka_consumer.poll(max_records=1)  # Consume only one record from the queue
            if list(record.items()):  # Ensures to have a message in the queue
                topic, value = list(record.items())[0]  # extract the information from the queue record
                kafka_consumer.commit()  # Remove the message consume from the queue
                output_offset = int(value[0][2]) + 1  # Export the message offset from the queue record
                output = value[0][6]  # Export the message from the queue record
            else:  # Case where there is no more message in the queue
                output = "None"
            kafka_consumer.pause()  # Make sleep the kafka consumer entity
            return {"message": output}
    else:
        return os.system("sleep 20")  # Case the pod is dying


"""Definition of the answer to http request GET /metrics/{offset}"""


@app.get("/metrics/{offset}")
def get_metrics(offset: int):
    global input_offset
    global nb_cons_wanted
    input_offset = offset
    nb_pod = len(act_cons_list)
    nb_waiting_work = input_offset - output_offset
    ratio = nb_waiting_work / nb_pod
    nb_cons_estimated = round(nb_cons_wanted * ratio)
    """Upper and lower limits of the number of pods"""
    if nb_cons_estimated >= 10:
        nb_cons_estimated = 10
    elif nb_cons_estimated <= 1:
        nb_cons_estimated = 1
    nb_cons_wanted = nb_cons_estimated
    print("-----METRICS-----")
    print("NB POD: " + str(nb_pod))
    print("NB WAITING WORK: " + str(nb_waiting_work))
    print("RATIO: " + str(ratio))
    print("NB CONSUMER WANTED: " + str(nb_cons_wanted))


#######################################################################################################################

"""When pacman start it run the fast api entity"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
