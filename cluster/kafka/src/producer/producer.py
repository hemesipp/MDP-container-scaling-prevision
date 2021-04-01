import threading
import time
import requests
import kafka


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        i = 0

        try:
            producer = kafka.KafkaProducer(bootstrap_servers='broker-0.broker.default.svc.cluster.local:9092')
        except kafka.errors.NoBrokersAvailable:
            time.sleep(30)
            self.run()

        while not self.stop_event.is_set():
            producer.send('topic_1', ("ciao" + str(i)).encode())
            offset = i + 1
            requests.get("http://pacman:80/metrics/" + offset)
            print("I am alive boys")
            i += 1
            time.sleep(1)

        producer.close()


def main():
    tasks = [
        Producer()
    ]

    # Start threads of a publisher/producer and a subscriber/consumer to 'topic_1' Kafka topic
    for t in tasks:
        t.start()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    main()
