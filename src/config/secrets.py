import os

from dotenv import load_dotenv

load_dotenv()


class Secrets:
    # API Key da sua aplicação
    API_KEY = os.getenv("API_KEY")

    # Langfuse
    LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_BASE_URL = os.getenv("LANGFUSE_BASE_URL")

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_NAME = os.getenv("DATABASE_NAME") or "database.sqlite3"
