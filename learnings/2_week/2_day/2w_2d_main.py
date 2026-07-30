
import gradio as gr
from utils.llm_utils.ollama_utils import create_ollama_client, OLLAMA_MODEL

llm_messages = []
user_messages = []

def memory_with_no_streaming_llm_calls(message: str) -> str:
    ollama = create_ollama_client()
    print(message)

    messages_to_send = [{"role": "system", "content": "You are an helpful assistant"}]
    for llm_message, user_message in zip(llm_messages, user_messages):
        messages_to_send.append({"role": "assistant", "content": llm_message})
        messages_to_send.append({"role": "user", "content": user_message})
    messages_to_send.append({"role": "user", "content": message})

    results = ollama.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=messages_to_send
    )
    response = results.choices[0].message.content
    llm_messages.append(response)
    user_messages.append(message)
    return response


def no_memory_with_streaming_llm_calls(message: str):
    ollama = create_ollama_client()
    print(message)

    messages_to_send = [
        {"role": "system", "content": "You are an helpful assistant"},
        {"role": "user", "content": message}
    ]
    stream = ollama.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=messages_to_send,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

if __name__ == '__main__':
    message_input = gr.Textbox(label="Your message: ", info="Enter a message for llm: ", lines=7)
    # message_output = gr.Textbox(label="Response: ", lines=8)
    message_output = gr.Markdown(label="Response: ")

    demo = gr.Interface(
        fn=no_memory_with_streaming_llm_calls,
        inputs=[message_input],
        outputs=[message_output],
        examples=["Hello", "Hi there"],
        flagging_mode="never"
    )
    demo.launch(inbrowser=True)


