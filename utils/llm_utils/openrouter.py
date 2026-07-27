import os

from openai import OpenAI

openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

# OPENROUTER_MODEL = "z-ai/glm-4.5"
# google/gemma-4-26b-a4b-it:free
# google/gemma-4-31b-it:free
OPENROUTER_MODEL = "google/gemma-4-26b-a4b-it:free"

def create_openrouter_client():
    OPENROUTER_URL = "https://openrouter.ai/api/v1"
    openrouter = OpenAI(base_url=OPENROUTER_URL, api_key=openrouter_api_key)
    return openrouter


def openrouter_text_completion(message: str):
    openrouter = create_openrouter_client()
    response = openrouter.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[{"role": "user", "content": message}]
    )

    return response.choices[0].message.content
