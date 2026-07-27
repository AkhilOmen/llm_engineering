from openai import OpenAI

LAMMA_3_2 = "llama3.2"
DEEPSEEK_R1_1__5_B = "deepseek-r1:1.5b"
MINIMAX_M3_CLOUD = "minimax-m3:cloud" # The best Open Source there is
KIMI_K3_CLOUD = "kimi-k3:cloud"  # For this we need Ollama subscription
GPT_OSS_20B = "gpt-oss:20b"

OLLAMA_MODEL = GPT_OSS_20B

def create_ollama_client():
    OLLAMA_BASE_URL = "http://localhost:11434/v1"

    """ api_key is dummy here as it's local we can pass anything"""
    ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

    return ollama


def ollama_text_completion(message: str):

    ollama = create_ollama_client()
    response = ollama.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": message}]
    )

    return response.choices[0].message.content
