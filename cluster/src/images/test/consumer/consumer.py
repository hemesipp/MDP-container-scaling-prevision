"""Only to test"""

"""Kafka consumer"""

import kafka
import time


def create_consumer():
    try:
        consumer = kafka.KafkaConsumer('topic_1',
                                       bootstrap_servers='broker-0.broker.default.svc.cluster.local:9092',
                                       group_id='mygroup',
                                       auto_offset_reset='earliest',
                                       consumer_timeout_ms=10000)
    except kafka.errors.NoBrokersAvailable:
        time.sleep(30)
        consumer = create_consumer()

    return consumer


def main():
    consumer = create_consumer()

    for msg in consumer:
        print(msg.value)


if __name__ == "__main__":
    main()
