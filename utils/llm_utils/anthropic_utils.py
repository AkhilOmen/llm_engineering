import os

from anthropic import Anthropic
from openai import OpenAI

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

def create_anthropic_client():
    ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1/"
    anthropic = OpenAI(base_url=ANTHROPIC_BASE_URL, api_key=anthropic_api_key)
    return anthropic


def anthropic_text_completion(message: str):
    anthropic = create_anthropic_client()
    response = anthropic.chat.completions.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{"role": "user", "content": message}]
    )

    return response.choices[0].message.content

# OR

def create_anthropic_client_and_text_completion_with_genai(message: str):
    client = Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{"role": "user", "content": message}],
        max_tokens=100
    )

    return response.content[0].text
