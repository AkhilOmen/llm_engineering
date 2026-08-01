import gradio as gr
import json

from utils.llm_utils.groq_utils import create_groq_client, GROQ_MODEL
from utils.llm_utils.ollama_utils import create_ollama_client, OLLAMA_MODEL

system_message = (
    "You are an helpful assistant for an Airline called FlightAI. "
    "Give short, courteous answers, no more than 1 sentence. Always be accurate. "
    "If you don't know the answer, say so."
)
groq = create_groq_client()
ollama = create_ollama_client()

# def basic_chat(message, history):
#     history = [{"role": h["role"], "content": h["content"]} for h in history]
#     messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
#
#     ollama = create_ollama_client()
#     response = ollama.chat.completions.create(
#         model=OLLAMA_MODEL,
#         messages=messages
#     )
#     return response.choices[0].message.content


def get_ticket_price(destination_city):
    city_ticket_price_mapping = {
        "london": "$700",
        "usa": "$500",
        "russia": "$800",
        "berlin": "$1600",
        "barcelona": "$4500",
    }

    price = city_ticket_price_mapping.get(destination_city.lower(), "Unknown place")
    return f"The price is {price} for the city {destination_city}"


price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False,
    }
}

tools = [
    {"type": "function", "function": price_function}
]


def handle_tool_call(message):
    response = {}
    tool_call = message.tool_calls[0]
    if tool_call.function.name == "get_ticket_price":
        arguments = json.loads(tool_call.function.arguments)
        destination_city = arguments.get("destination_city")
        price_details = get_ticket_price(destination_city)
        response = {
            "role": "tool",
            "content": price_details,
            "tool_call_id": tool_call.id,
        }
    return response


def handle_tool_calls(message):
    response = []
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            destination_city = arguments.get("destination_city")
            price_details = get_ticket_price(destination_city)
            response.append({
                "role": "tool",
                "content": price_details,
                "tool_call_id": tool_call.id,
            })
    return response


def chat_using_tools(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = ollama.chat.completions.create(model=OLLAMA_MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason=="tool_calls":
        tool_message = response.choices[0].message
        # tool_response = handle_tool_call(tool_message)
        tool_response = handle_tool_calls(tool_message)
        messages.append(tool_message)
        messages.extend(tool_response)
        response = ollama.chat.completions.create(model=OLLAMA_MODEL, messages=messages)

    return response.choices[0].message.content



if __name__ == '__main__':
    gr.ChatInterface(fn=chat_using_tools).launch(inbrowser=True)
