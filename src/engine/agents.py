from rag.vector import get_vectorstore


def search_finance(query: str):
    vs = get_vectorstore()
    return vs.similarity_search(query, k=5)
