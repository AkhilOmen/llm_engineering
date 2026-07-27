from utils.llm_utils.openai_utils import llm_is_stateless

if __name__ == '__main__':
    # encoding = tiktoken.encoding_for_model("gpt-4.1-mini")
    # # encoding = tiktoken.encoding_for_model("gpt-5")
    # tokens = encoding.encode("Hi my name is Akhil. I like chicken biryani a lot.")
    #
    # for token_id in tokens:
    #     word = encoding.decode([token_id])
    #     print(f"{token_id}={word}")
    #
    # # 12194=Hi
    # # 13232= Ak

    llm_is_stateless()
