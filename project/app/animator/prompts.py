import requests
from openai import OpenAI
from PIL import Image


def text_to_illustration(prompt, title):
    image_generated_response = OpenAI().images.generate(
        model="dall-e-3",
        prompt=f"{prompt}",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    print(image_generated_response)
    image_url = image_generated_response.data[0].url

    get_image_response = requests.get(image_url, stream=True)
    img = Image.open(get_image_response.raw)
    img.save(f"media/{title}.png")


def rewrite_prompt(prompt, change):
    response = OpenAI().chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are storybook writer familiar with \
                    rephrasing sentences into action phrases or background descriptions.",
            },
            {
                "role": "user",
                "content": f"convert the following sentence into {change}, \
                    no longer than five words: {prompt}",
            },
        ],
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content


def generate_character(prompt):
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
                        for the following story, limited to twenty words: {prompt}",
            },
        ],
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content


if __name__ == "__main__":
    SENTENCE = "He crosses the river to find his home."

    # character_prompt = """
    # 3-year old male hispanic child with brown hair and blue eyes wearing orange clothing
    # """
    # action_prompt = rewrite_prompt(SENTENCE, "an action verb")
    # background_prompt = rewrite_prompt(SENTENCE, "a background description")

    # TEST_PROMPT = f"""
    # Follow this prompt exactly: "Simple vector illustration of \
    # a {character_prompt}, {action_prompt}, {background_prompt}"

    # Do not add to the prompt. Use seed 42 for the generation.
    # """

    character_prompt = "At twenty-five, with dark chestnut hair, piercing blue eyes, and \
        dressed in earthy tones,"  # generate_character(SENTENCE)

    TEST_PROMPT = f"""
    Follow this prompt exactly: "Simple vector illustration of a {character_prompt}. {SENTENCE}"

    Do not add to the prompt. Use seed 42 for the generation.
    """

    text_to_illustration(TEST_PROMPT, "detailed_char_rewrite_1")
