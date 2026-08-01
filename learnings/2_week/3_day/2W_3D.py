import gradio as gr

from utils.llm_utils.groq_utils import create_groq_client, GROQ_MODEL



# def chat(message, history):
#     system_message = "You are an helpful assistant"
#     history = [{"role": h["role"], "content": h["content"]} for h in history]
#     messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
#
#     print("messages:", message)
#     print("history:", history)
#     print("\n\n\n")
#
#     groq = create_groq_client()
#
#     # response = groq.chat.completions.create(
#     #     model=GROQ_MODEL,
#     #     messages=messages
#     # )
#     # return response.choices[0].message.content
#
#     stream = groq.chat.completions.create(
#         model=GROQ_MODEL,
#         messages=messages,
#         stream=True
#     )
#     result = ""
#     for chunk in stream:
#         result += chunk.choices[0].delta.content or ""
#         yield result





def chat_and_inference_technique(message, history):
    system_message_v1 = (
        "You are an helpful assistant in a clothes store. You should try to gently encourage the customer to try items "
        "that are on sale. Hats are 60% off, and most other items are 50% off. For example, if the customer says "
        "'I am looking to buy a hat', you could reply something like, `Wonderful - we have lots of hats - including "
        "several that are part of our sales event'. Encourage them to buy hats if they are unsure what they want to buy, "
    )
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    if 'shirts' in message.lower():
        system_message_v1 += (
            "If the customer ask fors shirts, you should respond that shirts are not on sale today, "
            "but remind the customer to look at hats"
        )
    messages = [{"role": "system", "content": system_message_v1}] + history + [{"role": "user", "content": message}]

    groq = create_groq_client()
    stream = groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


if __name__ == '__main__':
    gr.ChatInterface(fn=chat_and_inference_technique).launch(inbrowser=True)