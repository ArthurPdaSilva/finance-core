import sqlite3
from typing import Any, List, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

from engine.agents import search_finance


class State(TypedDict):
    question: str
    answer: str
    docs: List[Any]


class EngineGraph:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")

    def retrieve_node(self, state: State):
        docs = search_finance(state["question"])
        return {"docs": docs}

    def answer_node(self, state: State):
        context = "\n\n".join([d.page_content for d in state["docs"]])
        q = state["question"]

        resp = self.llm.invoke(
            f"""
            Você é um assistente financeiro.
            Use APENAS as informações abaixo:

            {context}

            Pergunta: {q}
            Responda de forma direta e clara.
            """
        )

        return {"answer": resp.content}

    def build_graph(self):
        graph = StateGraph(State)

        graph.add_node("retrieve", self.retrieve_node)
        graph.add_node("answer", self.answer_node)

        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "answer")
        graph.set_finish_point("answer")

        conn = sqlite3.connect("state.db", check_same_thread=False)
        checkpointer = SqliteSaver(conn)

        return graph.compile(checkpointer=checkpointer)
