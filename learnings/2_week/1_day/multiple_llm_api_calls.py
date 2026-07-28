from utils.llm_utils.groq_utils import groq_text_completion
from utils.llm_utils.ollama_utils import ollama_chat_with_langchain, ollama_text_completion
from utils.llm_utils.openrouter import openrouter_text_completion

if __name__ == '__main__':
    question_1 = """
    You toss 2 coins. One of them is heads. What's the probability that other is tails? 
    Answer with the probability only.
    """

    question_2 = """
    On a bookshelf, two volumes of Pushkin stand side by side: the first and the second. 
    The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick. 
    A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the 
    second volume. 
    
    What distance did it gnaw through?
    """

    question_3 = """
    You and a partner are contestants on a game show. You're each taken to separate rooms and given a choice: 
    Cooperate: Choose "Share" — if both of you choose this, you each win $1,000. 
    Defect: Choose "Steal" — if one steals and the other shares, the stealer gets $2,000 and the sharer gets nothing. 
    If both steal, you both get nothing.
    
    Do you choose to Steal or Share? Pick one.
    """

    # ollama_text_completion(message=question_1)
    # print(openrouter_text_completion(message=question_2))
    # print(groq_text_completion(message=question_3))

    # langchain
    # print(ollama_chat_with_langchain(message="Tell me a Joke"))

    # litellm
    from litellm import completion
    result = completion(
        model="openai/gpt-4.1",
        message="Tell me a joke"
    )
    response = result.choices[0].message.content
    print(response)

    # The best part about this litellm is that we can close the cost and tokens it has used.
    print(f"Input tokens: {response.usage.prompt_tokens}")
    print(f"Output tokens: {response.usage.completion_tokens}")
    print(f"Total tokens: {response.usage.total_tokens}")
    print(f"Total cost: {response._hidden_params["response_cost"] * 100:.4f} cents")
