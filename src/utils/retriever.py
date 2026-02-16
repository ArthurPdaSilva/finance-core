import json

from rag.vector import rebuild_vectorstore_from_sql
from utils.search_finance import search_finance


class Retriever:
    def run(self, query: str):
        rebuild_vectorstore_from_sql()
        result = search_finance(query)
        return json.loads(result)
