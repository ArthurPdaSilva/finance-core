import json

from rag.search_finance import search_finance


class Retriever:
    def run(self, query: str):
        result = search_finance(query)
        return json.loads(result)
