import os

from openai import OpenAI

api_key = os.getenv('OPENAI_API_KEY')


def create_openai_client():
    openai = OpenAI(api_key=api_key)
    return openai


def openai_text_completion(text):
    openai = create_openai_client()

    messages = [
        {
            "role": "system",
            "content": "You are an assistant that analyzes the contents of a website, and provide a short summary, "
                       "ignore text that might be navigated related. Respond in markdown"
        },
        {
            "role": "user",
            "content": f"Here are the contents of a website. Provide a short summary of this website in markdown. "
                       f"If it includes news or announcements or reviews, then summarize them too. "
                       f""
                       f"{text}"
        }
    ]

    openai_response = openai.chat.completions.create(model="gpt-4.1-nano", messages=messages)
    parsed_response = openai_response.choices[0].message.content
    print(parsed_response)


def llm_is_stateless():
    openai = create_openai_client()

    # Case 1
    messages = [
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": "Hi my name is Akhil"}
    ]
    openai_response = openai.chat.completions.create(model="gpt-4.1-nano", messages=messages)
    parsed_response = openai_response.choices[0].message.content
    print(parsed_response)

    # response
    # Hi Akhil, How may I assist you.


    # Case 2
    messages = [
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": "What's my name"}
    ]
    openai_response = openai.chat.completions.create(model="gpt-4.1-nano", messages=messages)
    parsed_response = openai_response.choices[0].message.content
    print(parsed_response)

    # response
    # I don't have access to you personal information, how may I assist you.

    # Case 3
    messages = [
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": "Hi my name is Akhil"},
        {"role": "assistant", "content": "Hi Akhil, How may I help you today."},
        {"role": "user", "content": "What's my name"}
    ]
    openai_response = openai.chat.completions.create(model="gpt-4.1-nano", messages=messages)
    parsed_response = openai_response.choices[0].message.content
    print(parsed_response)

    # response
    # Your name is Akhil! How can I help you today