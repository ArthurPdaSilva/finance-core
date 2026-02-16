import json

from engine.tools.search_finance import search_finance_tool
from rag.vector import rebuild_vectorstore_from_sql


class RetrievalAgent:
    def run(self, query: str):
        rebuild_vectorstore_from_sql()
        result = search_finance_tool.func(query)
        return json.loads(result)
