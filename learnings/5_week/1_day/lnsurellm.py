import glob
import os
from pathlib import Path
import gradio as gr

from utils.llm_utils.ollama_utils import create_ollama_client, OLLAMA_BASE_URL, OLLAMA_MODEL

knowledge_base: dict = {}

def load_employees():
    filenames = glob.glob(
        os.path.expanduser(
            "~/Desktop/Personal/AI_Projects/llm_engineering/learnings/5_week/knowledge-base/employees/*"
        )
    )

    for filename in filenames:
        name = Path(filename).stem.split(" ")[-1]
        with open(filename, "r", encoding="utf-8") as f:
            knowledge_base[name.lower()] = f.read()


def load_products():
    filenames = glob.glob(
        os.path.expanduser(
            "~/Desktop/Personal/AI_Projects/llm_engineering/learnings/5_week/knowledge-base/products/*"
        )
    )

    for filename in filenames:
        name = Path(filename).stem
        with open(filename, "r", encoding="utf-8") as f:
            knowledge_base[name.lower()] = f.read()


SYSTEM_PREFIX = """
    You represent Insurerllm, the Insurance Tech company. 
    You are an expert answering questions about Insurerllm; it's employees and it's products.
    You are provided with additional context that might be relevant to the user's question.
    Give brief and accurate answer. If you don't know the answer say so.

    Relevant context:
    """


def get_relevant_context(message: str):
    load_employees()
    load_products()

    text = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())
    words = text.lower().split()
    return [knowledge_base[word] for word in words if word in knowledge_base]


def get_additional_context(message):
    relevant_context = get_relevant_context(message)
    if not relevant_context:
        result = "There is no data for given message"
    else:
        result = "The following additional context might be relevant in answering the user's question: \n\n"
        result += "\n\n".join(relevant_context)

    return result


def chat_fn(message, history):
    system_message = SYSTEM_PREFIX + get_additional_context(message)
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    ollama = create_ollama_client()
    response = ollama.chat.completions.create(model=OLLAMA_MODEL, messages=messages)
    return response.choices[0].message.content


if __name__ == '__main__':
    gr.ChatInterface(fn=chat_fn).launch(inbrowser=True)

