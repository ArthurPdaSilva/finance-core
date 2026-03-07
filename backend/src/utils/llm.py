from langchain_openai import ChatOpenAI


def make_llm():
    return ChatOpenAI(model="gpt-4o-mini")
