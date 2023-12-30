import os
import json
import time
from tqdm import trange

from kafka import KafkaProducer
from constants import KAFKA_SERVER_URL, VIDEO_UPLOADED_TOPIC, INPUT_FILEPATH

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER_URL,
    value_serializer=lambda m: json.dumps(m).encode("utf-8"),
)


def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    print("Error occured: ", exc_info=excp)


def send_event(topic, data):
    producer.send(topic, value=data).add_callback(on_send_success).add_errback(
        on_send_error
    )


def main():
    total = 2
    for i in trange(1, total):
        print("-----------------------------------")
        print(f"Uploading video {i} of {total-1}...")
        send_event(VIDEO_UPLOADED_TOPIC, data={"filepath": INPUT_FILEPATH})
        time.sleep(1)


if __name__ == "__main__":
    main()
