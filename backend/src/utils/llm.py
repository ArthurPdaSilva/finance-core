import os

from langchain_openai import ChatOpenAI


def make_llm():
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    kwargs = {
        "model": os.getenv(
            "OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free"
        ),
        "api_key": openrouter_api_key or os.getenv("OPENAI_API_KEY"),
    }

    if openrouter_api_key:
        kwargs["base_url"] = os.getenv(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
        )

    return ChatOpenAI(**kwargs)
