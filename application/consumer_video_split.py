import os
import json
import subprocess

from kafka import KafkaConsumer
from constants import (
    KAFKA_SERVER_URL,
    VIDEO_UPLOADED_TOPIC,
    MERGE_VIDEO_TOPIC,
    CHUNKS_PATH,
)
from producer import send_event

consumer = KafkaConsumer(
    VIDEO_UPLOADED_TOPIC,
    bootstrap_servers=KAFKA_SERVER_URL,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print(f"Listening on topic: {VIDEO_UPLOADED_TOPIC} ...")


def split_video(input_file, chunk_duration_sec=10):
    # Create chunks folder if it doesn't exist
    if not os.path.exists(CHUNKS_PATH):
        os.makedirs(CHUNKS_PATH)

    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_file,
        "-c",
        "copy",
        "-map",
        "0",
        "-segment_time",
        f"00:00:{chunk_duration_sec}",
        "-f",
        "segment",
        "-reset_timestamps",
        "1",
        os.path.join(CHUNKS_PATH, "chunk%03d.mp4"),
    ]

    subprocess.run(ffmpeg_command)


while True:
    for message in consumer:
        print(f"- message in A: {message.value}")
        split_video(input_file=message.value["filepath"])
        # send event to merge the chunks
        data = {"folderpath": CHUNKS_PATH}
        send_event(MERGE_VIDEO_TOPIC, data)
