from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from rag.rag_sql import sql_to_documents


def get_vectorstore():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(persist_directory="chroma_financas", embedding_function=embeddings)


def rebuild_vectorstore_from_sql():
    vs = get_vectorstore()

    vs.reset_collection()

    docs = sql_to_documents()
    vs.add_documents(docs)

    print("Embeddings financeiros atualizados!")
