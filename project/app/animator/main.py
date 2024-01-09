import logging
import os
import time

import nltk
from openai import OpenAI

from app.animator.Generator import Generator

# config logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("main.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def generate_video_locally(script: str, video_id: str) -> None:
    # TODO: Add more specific exception handling for different types of errors
    if not os.path.exists("media"):
        os.mkdir("media")

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    video_path = f"media/{video_id}.mp4"

    if not os.path.exists(video_path):
        st = time.time()
        pst = time.process_time()

        Generator(
            OpenAIClient=OpenAI(), script=script, video_id=video_id
        ).create_animation_from_script()

        et = time.time()
        pet = time.process_time()

        elapsed_time = et - st
        process_elapsed_time = pet - pst

        print(f"Execution time: {elapsed_time} seconds")
        print(f"CPU Execution time: {process_elapsed_time} seconds")


if __name__ == "__main__":
    id = "7ca2688a-264d-4c6e-9766-cc48ddd3ffb3"
    generate_video_locally(
        "A man founds out that his wallet was stolen. He ran around the city to find the thief. \
            But he was too slow and failed to find it.",
        id,
    )
