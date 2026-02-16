from langfuse import Langfuse

from config.secrets import Secrets

langfuse = (
    Langfuse(
        public_key=Secrets.LANGFUSE_PUBLIC_KEY,
        secret_key=Secrets.LANGFUSE_SECRET_KEY,
        host=Secrets.LANGFUSE_BASE_URL,
    ),
)
