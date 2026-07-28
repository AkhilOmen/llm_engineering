import os

from openai import OpenAI

groq_api_key = os.getenv('GROQ_API_KEY')

GROQ_MODEL = "openai/gpt-oss-20b"

def create_groq_client():
    GROQ_BASE_URL = "https://api.groq.com/openai/v1"
    groq = OpenAI(base_url=GROQ_BASE_URL, api_key=groq_api_key)
    return groq


def groq_text_completion(message: str):
    groq = create_groq_client()
    response = groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": message}]
    )

    return response.choices[0].message.content
