import json

from langchain.tools import tool

from rag.vector import get_vectorstore


@tool
def search_finance_tool(query: str):
    """
    Realiza uma busca semântica em um banco de dados de documentos financeiros,
    retornando os trechos mais relevantes com base na similaridade do conteúdo.

    Args:
        query: Consulta em linguagem natural usada para buscar informações financeiras relevantes.
    """
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=5)
    return json.dumps([d.page_content for d in docs])
