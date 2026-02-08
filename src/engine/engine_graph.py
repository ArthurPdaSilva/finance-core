import sqlite3
from typing import Any, List, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

from engine.agents.answer_agent import AnswerAgent
from engine.agents.retrieval_agent import RetrievalAgent


class State(TypedDict):
    question: str
    answer: str
    docs: List[Any]


class EngineGraph:
    def __init__(self):
        self.retrieval_agent = RetrievalAgent()
        self.answer_agent = AnswerAgent()

    def retrieve_node(self, state: State):
        docs = self.retrieval_agent.run(state["question"])
        return {"docs": docs}

    def answer_node(self, state: State):
        final_answer = self.answer_agent.run(
            question=state["question"],
            docs=state["docs"],
        )
        return {"answer": final_answer}

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
