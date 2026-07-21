import os

from openai import OpenAI

google_api_key = os.getenv('GOOGLE_API_KEY')

def create_gemini_client():
    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
    gemini = OpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
    return gemini


def gemini_text_completion(message: str):
    gemini = create_gemini_client()
    response = gemini.chat.completions.create(
        model="gemini-2.5-pro",
        messages=[{"role": "user", "content": message}]
    )

    return response.choices[0].message.content
