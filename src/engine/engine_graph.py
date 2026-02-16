import sqlite3
from typing import Any, List, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

from engine.agents.answer_agent import AnswerAgent
from engine.agents.routing_agent import RoutingAgent
from engine.agents.sql_agent import SqlAgent
from rag.retriever import Retriever
from rag.vector import rebuild_vectorstore_from_sql


class State(TypedDict):
    question: str
    answer: str
    docs: List[Any]


class EngineGraph:
    def __init__(self):
        self.routing_agent = RoutingAgent()
        self.answer_agent = AnswerAgent()
        self.sql_agent = SqlAgent()
        self.retriever = Retriever()

    def route_node(self, state: State):
        intent = self.routing_agent.run(state["question"])
        return {"intent": intent}

    def retriever_node(self, state: State):
        docs = self.retriever.run(
            state["question"],
        )
        return {"docs": docs}

    def answer_node(self, state: State):
        final_answer = self.answer_agent.run(
            question=state["question"],
            docs=state["docs"],
        )
        return {"answer": final_answer}

    def sql_node(self, state: State):
        sql_result = self.sql_agent.run(
            state["question"],
        )
        rebuild_vectorstore_from_sql()
        return {"answer": sql_result}

    def build_graph(self):
        graph = StateGraph(State)

        graph.add_node("route", self.route_node)
        graph.add_node("rag", self.retriever_node)
        graph.add_node("answer", self.answer_node)
        graph.add_node("sql", self.sql_node)

        graph.set_entry_point("route")

        graph.add_conditional_edges(
            "route",
            lambda s: s["intent"],
            {
                "rag": "rag",
                "sql": "sql",
            },
        )

        graph.add_edge("rag", "answer")

        # Finais
        graph.set_finish_point("answer")
        graph.set_finish_point("sql")

        conn = sqlite3.connect("state.db", check_same_thread=False)
        checkpointer = SqliteSaver(conn)
        return graph.compile(
            checkpointer=checkpointer,
        )
