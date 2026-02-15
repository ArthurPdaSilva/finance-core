import os

from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

langfuse = (
    Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_BASE_URL"),
    ),
)
