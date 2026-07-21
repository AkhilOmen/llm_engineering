from openai import OpenAI


def create_ollama_client():
    OLLAMA_BASE_URL = "http://localhost:11434/v1"

    """ api_key is dummy here as it's local we can pass anything"""
    ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

    return ollama


def ollama_text_completion(message: str):
    LAMMA_3_2 = "llama3.2"
    DEEPSEEK_R1_1__5_B = "deepseek-r1:1.5b"

    ollama = create_ollama_client()
    response = ollama.chat.completions.create(
        model=DEEPSEEK_R1_1__5_B,
        messages=[{"role": "user", "content": message}]
    )

    return response.choices[0].message.content
