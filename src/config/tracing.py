from langfuse.langchain import CallbackHandler
from langgraph_sdk import get_client

langfuse = get_client()
langfuse_handler = CallbackHandler()
