import logging
import os

import ffprobe  # noqa: F401
import requests
from elevenlabs import generate, save, set_api_key
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment

from tenacity import (  # isort:skip
    retry,
    stop_after_attempt,
    wait_fixed,
)

from moviepy.editor import (  # isort:skip
    ImageClip,
    concatenate_videoclips,
    AudioFileClip,
)


# config logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("generation.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


set_api_key(os.environ.get("ELEVENLABS"))


class Animator:
    def __init__(self, OpenAIClient, text, video_path):
        self.OpenAIClient = OpenAIClient
        self.text = text
        self.video_path = video_path

        if not os.path.exists(self.video_path):
            os.mkdir(self.video_path)

    # rate limit by OpenAI at 5 images / min + 20 seconds for caution (generation time)
    @retry(wait=wait_fixed(80), stop=stop_after_attempt(3))
    def _text_to_illustration(self):
        if not os.path.exists(f"{self.video_path}/illustration__{self.text}__.png"):
            managed_prompt = f"""
                Follow this prompt exactly, "flat simple vector illustrations style on WHITE background: {self.text}”.

                Do not add to the prompt.
            """

            image_generated_response = self.OpenAIClient.images.generate(
                model="dall-e-3",
                prompt=f"{managed_prompt}",
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = image_generated_response.data[0].url
            logger.info("Illustration created: %s", image_url)

            get_image_response = requests.get(image_url, stream=True)
            img = Image.open(get_image_response.raw)
            img.save(f"{self.video_path}/illustration__{self.text}__.png")

        return Image.open(f"{self.video_path}/illustration__{self.text}__.png")

    def _get_average_color_image(self, illustration):
        try:
            i = illustration
            h = i.histogram()

            # split into red, green, blue
            r = h[0:256]
            g = h[256 : 256 * 2]  # noqa: E203
            b = h[256 * 2 : 256 * 3]  # noqa: E203

            # perform the weighted average of each channel:
            # the *index* is the channel value, and the *value* is its weight
            return (
                round(sum(i * w for i, w in enumerate(r)) / sum(r)),
                round(sum(i * w for i, w in enumerate(g)) / sum(g)),
                round(sum(i * w for i, w in enumerate(b)) / sum(b)),
            )
        except Exception as e:
            logger.exception(
                "Error getting color for folder %s - %s", self.video_path, e
            )

    def _split_text_for_captioning(self):
        try:
            MAX_LENGTH_CAPTION = 20

            caption_chunks = []
            text_chunks = self.text.split(" ")
            current_text = ""

            for text_chunk in text_chunks:
                if len(current_text) == 0:
                    current_text = text_chunk
                    continue

                if len(current_text + text_chunk) > MAX_LENGTH_CAPTION:
                    caption_chunks.append(current_text)
                    current_text = text_chunk

                else:
                    current_text += f" {text_chunk}"

            caption_chunks.append(current_text)

            logger.info("Caption chunks: %s", caption_chunks)

            return caption_chunks

        except Exception as e:
            logger.exception(
                "Error splitting captions for folder %s - %s", self.video_path, e
            )

    def _text_to_audio(self, caption_chunk):
        try:
            EMPIRICAL_VARIABLE_FOR_TRIMMING_AUDIO = (
                25  # split audio chunks trimmed for smoother effect
            )

            if not os.path.exists(f"{self.video_path}/__{caption_chunk}__.mp3"):
                audio = generate(
                    text=caption_chunk, voice="Josh", model="eleven_multilingual_v2"
                )

                logger.info("Generating audio: %s", caption_chunk)

                # saving audio file from ElevenLabs to import into pydub format
                save(audio, f"{self.video_path}/__{caption_chunk}__.mp3")

            audio_chunk = AudioSegment.from_mp3(
                f"{self.video_path}/__{caption_chunk}__.mp3"
            )
            audio_chunk_trimmed = audio_chunk[
                0 : audio_chunk.duration_seconds * 1000  # noqa: E203
                - len(caption_chunk) * EMPIRICAL_VARIABLE_FOR_TRIMMING_AUDIO
            ]

            return audio_chunk_trimmed

        except Exception as e:
            logger.exception(
                "Error generating audio for folder %s - %s", self.video_path, e
            )

    def _draw_text_on_image(self, img, text, text_color):
        try:
            fnt = ImageFont.truetype("Fonts/Arvo-BoldItalic.ttf", 70)

            draw = ImageDraw.Draw(img)
            draw.text(
                (540, 400),
                text,
                font=fnt,
                anchor="ms",
                fill=text_color,
                stroke_width=5,
                stroke_fill="white",
            )
            logger.info("Adding text to illustration: %s", text)

            return img

        except Exception as e:
            logger.exception(
                "Error drawing text for folder %s - %s", self.video_path, e
            )

    def create_animation(self):
        try:
            illustration = self._text_to_illustration()
            average_image_color = self._get_average_color_image(illustration)

            caption_chunks = self._split_text_for_captioning()
            audio_chunks = []
            caption_image_chunks = []

            for caption_chunk in caption_chunks:
                audio_chunk = self._text_to_audio(caption_chunk)
                audio_chunks.append(audio_chunk)

                image_canvas = Image.new(mode="RGB", size=(1080, 1920), color="white")
                image_canvas.paste(illustration, (30, 450))

                illustration_with_text = self._draw_text_on_image(
                    image_canvas, caption_chunk, average_image_color
                )
                illustration_with_text.save(
                    f"{self.video_path}/__{caption_chunk}__.png"
                )

                caption_image_chunk = ImageClip(
                    f"{self.video_path}/__{caption_chunk}__.png"
                ).set_duration(audio_chunk.duration_seconds)
                caption_image_chunks.append(caption_image_chunk)

            self._text_to_audio(
                self.text
            )  # full sentence audio used for smoother effect

            # moviepy
            audioclips = AudioFileClip(f"{self.video_path}/__{self.text}__.mp3")
            videoclips = concatenate_videoclips(caption_image_chunks, method="compose")

            logger.info("Audio Duration: %f", audioclips.duration)
            logger.info("Video Duration: %f", videoclips.duration)

            audiovisual = videoclips.set_audio(audioclips)
            audiovisual.write_videofile(
                f"{self.video_path}/__{self.text}__.mp4", audio_codec="aac", fps=24
            )

            logger.info("Animation created: %s", self.text)

        except Exception as e:
            logger.exception(
                "Error creating animation for folder %s - %s", self.video_path, e
            )
