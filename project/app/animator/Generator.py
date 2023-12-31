import concurrent
import logging
import os
import shutil

import nltk
from moviepy.editor import VideoFileClip, concatenate_videoclips
from openai import OpenAI

from app.animator.Animator import Animator
from app.animator.helper import upload_video_to_cloud

# config logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("generation.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def create_animation_from_sentence(idx_and_text_and_folder):
    """
    Function to support parallel processing
    """

    idx, text, video_path, avatar_prompt = idx_and_text_and_folder

    text_stripped = text.strip()

    if not os.path.exists(f"{video_path}/{idx}/__{text_stripped}__.mp4"):
        Animator(
            OpenAIClient=OpenAI(),
            text=text_stripped,
            video_path=f"{video_path}/{idx}",
            avatar_prompt=avatar_prompt,
        ).create_animation()

    return f"{video_path}/{idx}/__{text_stripped}__.mp4"


class Generator:
    def __init__(self, OpenAIClient, script, video_id):
        self.media_folder = "media"
        self.video_path = f"{self.media_folder}/{video_id}"
        self.script = script
        self.sentences = self._split_text_into_sentences(script)
        self.OpenAIClient = OpenAIClient
        self.video_id = video_id
        self.progress = 0

        if not os.path.exists(self.video_path):
            os.mkdir(self.video_path)

    def _clear(self):
        if os.path.exists(self.video_path):
            shutil.rmtree(self.video_path)

            logger.info("%s - Deleting files...", self.video_id)

    def _split_text_into_sentences(self, script):
        return nltk.sent_tokenize(script)

    def _update_task_progress(self, future):
        self.progress += 1

        logger.info(
            "Video generation progress: %f", self.progress / len(self.sentences)
        )

    def create_avatar_from_script(self):
        # TODO: Add exception handling
        response = OpenAI().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are storybook writer familiar with writing \
                        description of characters from a storyline.",
                },
                {
                    "role": "user",
                    "content": f"Write a character description with details like \
                        age, hair color, eye color, race, clothing color, gender \
                            for the following story, limited to twenty words: {self.script}",
                },
            ],
        )

        avatar_prompt = response.choices[0].message.content

        logger.info("Avatar created: %s", avatar_prompt)

        return avatar_prompt

    def create_animation_from_script(self, keep_files=False):
        logger.info("%s - Starting animation...", self.video_id)

        videoclips = []

        avatar_prompt = self.create_avatar_from_script()

        try:
            inputs = [
                list(tup) + [self.video_path] + [avatar_prompt]
                for tup in enumerate(self.sentences)
            ]

            with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
                futures = [
                    executor.submit(
                        create_animation_from_sentence, idx_and_text_and_folder
                    )
                    for idx_and_text_and_folder in inputs
                ]

                for future in futures:
                    future.add_done_callback(self._update_task_progress)

                videoclip_names = [future.result() for future in futures]
                videoclips = [
                    VideoFileClip(videoclip_name) for videoclip_name in videoclip_names
                ]

        except Exception as e:
            logger.exception("%s - Error parallel processing - %s", self.video_id, e)

        try:
            composed_videoclip = concatenate_videoclips(videoclips)
            composed_videoclip.write_videofile(
                f"{self.media_folder}/{self.video_id}.mp4", audio_codec="aac", fps=24
            )

            if not keep_files:
                self._clear()

        except Exception as e:
            logger.exception("%s - Error creating video - %s", self.video_id, e)

        upload_video_to_cloud(f"{self.media_folder}/{self.video_id}.mp4", self.video_id)
