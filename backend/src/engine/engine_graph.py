import sqlite3
from typing import Any, List, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

from engine.agents.answer_agent import AnswerAgent
from engine.agents.chat_manager_agent import ChatManagerAgent
from engine.agents.greeting_agent import GreetingAgent
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
    chat_token: int | None


class EngineGraph:
    def __init__(self):
        self.routing_agent = RoutingAgent()
        self.answer_agent = AnswerAgent()
        self.sql_agent = SqlAgent()
        self.greeting_agent = GreetingAgent()
        self.retriever = Retriever()
        self.synthesis_agent = SynthesisAgent()
        self.chat_manager_agent = ChatManagerAgent()

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
        history = self.get_history_formatted(state)
        final = self.synthesis_agent.run(state["question"], [state["answer"]], history)
        return {"answer": final}

    def greeting_node(self, state: State):
        history = self.get_history_formatted(state)
        result = self.greeting_agent.run(state["question"], history)

        return {"answer": result}

    def chat_manager_node(self, state: State):
        history = self.get_history_formatted(state)
        chat_token = self.chat_manager_agent.run(
            state["question"], state["answer"], state["chat_token"], history
        )
        return {"chat_token": chat_token}

    def build_graph(self):
        graph = StateGraph(State)
        graph.add_node("chat_manager", self.chat_manager_node)
        graph.add_node("route", self.route_node)
        graph.add_node("rag", self.retriever_node)
        graph.add_node("answer", self.answer_node)
        graph.add_node("sql", self.sql_node)
        graph.add_node("synthesis", self.synthesis_node)
        graph.add_node("greeting", self.greeting_node)

        graph.set_entry_point("route")

        graph.add_conditional_edges(
            "route",
            lambda s: s["intent"],
            {"rag": "rag", "sql": "sql", "greeting": "greeting"},
        )

        # RAG → ANSWER → SYNTHESIS
        graph.add_edge("rag", "answer")
        graph.add_edge("answer", "synthesis")

        # SQL → SYNTHESIS
        graph.add_edge("sql", "synthesis")

        # SYNTHESIS → CHAT_MANAGER
        graph.add_edge("synthesis", "chat_manager")

        # GREETING → CHAT_MANAGER
        graph.add_edge("greeting", "chat_manager")

        # FINAL
        graph.set_finish_point("chat_manager")

        conn = sqlite3.connect("state.db", check_same_thread=False)
        checkpointer = SqliteSaver(conn)
        return graph.compile(
            checkpointer=checkpointer,
        )
