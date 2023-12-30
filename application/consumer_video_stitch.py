import os
import json
import subprocess

from kafka import KafkaConsumer
from constants import (
    KAFKA_SERVER_URL,
    MERGE_VIDEO_TOPIC,
    OUTPUT_FILENAME,
    OUTPUT_PATH,
)

consumer = KafkaConsumer(
    MERGE_VIDEO_TOPIC,
    bootstrap_servers=KAFKA_SERVER_URL,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print(f"Listening on topic: {MERGE_VIDEO_TOPIC} ...")


def merge_video_chunks(input_folder, output_file):
    # Create output folder if it doesn't exist
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    # List all files in the input folder
    input_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".mp4")])

    # Create a file list for ffmpeg concatenation
    file_list_path = "file_list.txt"
    with open(file_list_path, "w") as file_list:
        for input_file in input_files:
            file_list.write(f"file '{os.path.join(input_folder, input_file)}'\n")

    # Use ffmpeg to concatenate the video files
    ffmpeg_command = [
        "ffmpeg",
        "-y", # overwrite
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        file_list_path,
        "-c",
        "copy",
        os.path.join(OUTPUT_PATH, output_file),
    ]

    subprocess.run(ffmpeg_command)

    # Remove the temporary file list
    os.remove(file_list_path)


while True:
    for message in consumer:
        print(f"- message in {MERGE_VIDEO_TOPIC}: {message.value}")
        chunks_path = message.value["folderpath"]
        merge_video_chunks(input_folder=chunks_path, output_file=OUTPUT_FILENAME)
        print("Done!")
