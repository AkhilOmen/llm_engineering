import gradio
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_openai import ChatOpenAI

from core.config import settings
from utils.constants import RETRIEVAL_K
from utils.ingest import ingestion

embeddings_insurellm = ingestion(
    folders_path="~/Desktop/Personal/AI_Projects/llm_engineering/learnings/5_week/knowledge-base/*"
)
retriever = embeddings_insurellm.as_retriever()
llm = ChatOpenAI(model="gpt-4.1-nano", api_key=settings.OPENAI_API_KEY, temperature=0)


def fetch_context(question: str):
    context = retriever.invoke(question, k=RETRIEVAL_K)
    return context


def combine_questions(question: str, history: list[dict]):
    prior = "\n".join(
        item['text']
        for m in history
        if m['role'] == 'user'
        for item in m['content']
    )
    questions_str = prior + "\n" + question

    return questions_str


def basic_RAG_functionality(question: str, history: list[dict]):
    # Retrieval Docs
    all_questions_str = combine_questions(question, history)
    docs = fetch_context(all_questions_str)

    # LLM CALL
    SYSTEM_PROMPT_TEMPLATE = f"""
    You are knowledgeable, friendly assistant representing the company Insurellm.
    You are chatting with user about Insurellm.
    If relevant, use the given context to answer the question.
    If you don't know the answer, say so.
    Context:
    {{context}}
    """

    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)
    messages: list = [SystemMessage(content=system_prompt)]
    messages.extend(convert_to_messages(history))
    messages.append(HumanMessage(content=question))
    responses = llm.invoke(messages)

    return responses.content


if __name__ == '__main__':
    gradio.ChatInterface(fn=basic_RAG_functionality).launch(inbrowser=True)
