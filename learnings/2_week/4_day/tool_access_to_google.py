import json

import gradio as gr

from utils.llm_utils.groq_utils import create_groq_client, GROQ_MODEL
from utils.serp_api_utils import SerpSearchClient

system_message = (
    "You are an helpful assistant. "
    "Give short, courteous answers, no more than 1 sentence. Always be accurate. "
    "If you don't know the answer, say so."
)
groq = create_groq_client()

def google_search(query):
    serp_client = SerpSearchClient()
    return serp_client.search(query)

google_search_function = {
    "name": "google_search",
    "description": "Get the google search results",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query that the customer wants the answer for",
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    }
}

tools = [
    {"type": "function", "function": google_search_function}
]


def handle_tool_call(message):
    response = {}
    tool_call = message.tool_calls[0]
    if tool_call.function.name == "google_search":
        arguments = json.loads(tool_call.function.arguments)
        query = arguments.get("query")
        query_answers = google_search(query)
        response = {
            "role": "tool",
            "content": json.dumps(query_answers, ensure_ascii=False),
            "tool_call_id": tool_call.id,
        }
    return response


def chat_with_google_support(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = groq.chat.completions.create(model=GROQ_MODEL, messages=messages, tools=tools)

    # if response.choices[0].finish_reason == "tool_calls":
    while response.choices[0].finish_reason == "tool_calls":
        tool_message = response.choices[0].message
        tool_response = handle_tool_call(tool_message)
        messages.append(tool_message)
        messages.append(tool_response)
        # response = groq.chat.completions.create(model=GROQ_MODEL, messages=messages)
        response = groq.chat.completions.create(model=GROQ_MODEL, messages=messages, tools=tools)

    return response.choices[0].message.content



if __name__ == '__main__':
    gr.ChatInterface(fn=chat_with_google_support).launch(inbrowser=True)