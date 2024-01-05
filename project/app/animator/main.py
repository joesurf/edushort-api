import time

from openai import OpenAI

from app.animator.Generator import Generator
from app.animator.Animator import Animator


SCRIPT = """
    Here’s what I.
    """

# Separate functions
# TODO: Generate video - input [script, id] output [video file] temp [media]
# TODO: Upload video - input [video file] output [boolean success]
# TODO: Send email update - input [user id] output [boolean success]
# TODO: Update credits - input [user id] output [credits]


if __name__ == "__main__":
    st = time.time()
    pst = time.process_time()

    # Generator(OpenAI(), SCRIPT)
    Animator(OpenAI(), "A blue pikachu", "media/0").create_animation()

    et = time.time()
    pet = time.process_time()

    elapsed_time = et - st
    process_elapsed_time = pet - pst

    print(f"Execution time: {elapsed_time} seconds")
    print(f"CPU Execution time: {process_elapsed_time} seconds")
