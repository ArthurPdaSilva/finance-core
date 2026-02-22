import sqlite3
from typing import Any, List, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

from engine.agents.answer_agent import AnswerAgent
from engine.agents.routing_agent import RoutingAgent
from engine.agents.sql_agent import SqlAgent
from engine.agents.synthesis_agent import SynthesisAgent
from rag.retriever import Retriever
from rag.vector import rebuild_vectorstore_from_sql
from utils.parse_history import parse_history


class State(TypedDict):
    question: str
    answer: str
    docs: List[Any]
    chat_history: List[str]


class EngineGraph:
    def __init__(self):
        self.routing_agent = RoutingAgent()
        self.answer_agent = AnswerAgent()
        self.sql_agent = SqlAgent()
        self.retriever = Retriever()
        self.synthesis_agent = SynthesisAgent()

    def get_history_formatted(self, state: State):
        return parse_history(state["chat_history"])

    def route_node(self, state: State):
        history = self.get_history_formatted(state)
        intent = self.routing_agent.run(state["question"], history)
        return {"intent": intent}

    def retriever_node(self, state: State):
        rebuild_vectorstore_from_sql()
        docs = self.retriever.run(
            state["question"],
        )
        return {"docs": docs}

    def answer_node(self, state: State):
        history = self.get_history_formatted(state)
        final_answer = self.answer_agent.run(
            question=state["question"], docs=state["docs"], chat_history=history
        )
        return {"answer": final_answer}

    def sql_node(self, state: State):
        history = self.get_history_formatted(state)
        sql_result = self.sql_agent.run(state["question"], history)

        return {"answer": sql_result}

    def synthesis_node(self, state: State):
        final = self.synthesis_agent.run([state["answer"]])
        return {"answer": final}

    def build_graph(self):
        graph = StateGraph(State)

        graph.add_node("route", self.route_node)
        graph.add_node("rag", self.retriever_node)
        graph.add_node("answer", self.answer_node)
        graph.add_node("sql", self.sql_node)
        graph.add_node("synthesis", self.synthesis_node)

        graph.set_entry_point("route")

        graph.add_conditional_edges(
            "route",
            lambda s: s["intent"],
            {
                "rag": "rag",
                "sql": "sql",
            },
        )

        # RAG → ANSWER → SYNTHESIS
        graph.add_edge("rag", "answer")
        graph.add_edge("answer", "synthesis")

        # SQL → SYNTHESIS
        graph.add_edge("sql", "synthesis")

        # FINAL
        graph.set_finish_point("synthesis")

        conn = sqlite3.connect("state.db", check_same_thread=False)
        checkpointer = SqliteSaver(conn)
        return graph.compile(
            checkpointer=checkpointer,
        )
