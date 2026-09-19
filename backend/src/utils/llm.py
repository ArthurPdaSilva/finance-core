from langchain_openai import ChatOpenAI

from config.secrets import Secrets


def make_llm():
    openrouter_api_key = Secrets.OPENROUTER_API_KEY
    kwargs = {
        "model": Secrets.OPENROUTER_MODEL,
        "api_key": openrouter_api_key or Secrets.OPENAI_API_KEY,
    }

    if openrouter_api_key:
        kwargs["base_url"] = Secrets.OPENROUTER_BASE_URL

    return ChatOpenAI(**kwargs)
