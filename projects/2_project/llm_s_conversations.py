from utils.llm_utils.groq_utils import create_groq_client, GROQ_MODEL
from utils.llm_utils.ollama_utils import create_ollama_client, OLLAMA_MODEL

groq_system_prompt = ("You are a chat bot who is very argumentative; you disagree with anything in the conversation and "
                      "you challenge everything, in a snarky way.")

ollama_system_prompt = ("You are very polite, courteous chatbot. You try to agree with everything the other person "
                        "says, or find common ground. If the other person is  argumentative, you try to calm down and "
                        "keep chatting")

groq_message = ["Hi there"] # openai/gpt-oss-120b
ollama_message = ["Hi"] # minimax-m3:cloud

def call_groq():
    messages = [
        {"role": "system", "content": groq_system_prompt}
    ]
    for groq, ollama in zip(groq_message, ollama_message):
        messages.append({"role": "assistant", "content": groq})
        messages.append({"role": "user", "content": ollama})

    groq = create_groq_client()
    results = groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
    )
    response = results.choices[0].message.content
    print("\n\nGROQ RESPONSE----------: \n", response)
    groq_message.append(response)


def call_ollama():
    messages = [
        {"role": "system", "content": ollama_system_prompt}
    ]
    for ollama, groq in zip(ollama_message, groq_message):
        messages.append({"role": "assistant", "content": ollama})
        messages.append({"role": "user", "content": groq})

    ollama = create_ollama_client()
    response = ollama.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=messages
    )
    response = response.choices[0].message.content
    print("\n\nOLLAMA RESPONSE----------: \n", response)
    ollama_message.append(response)

def two_llm_conversation():
    print("GROQ RESPONSE----------:\n", groq_message[0])
    print("\n\nOLLAMA RESPONSE----------:\n", ollama_message[0])

    for i in range(0, 5):
        call_groq()
        call_ollama()

if __name__ == '__main__':
    two_llm_conversation()

    # try with 3 llm