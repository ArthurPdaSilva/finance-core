import sqlite3
from typing import Any, List, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

from engine.agents.answer_agent import AnswerAgent
from engine.agents.retrieval_agent import RetrievalAgent
from engine.agents.sql_agent import SqlAgent
from rag.vector import rebuild_vectorstore_from_sql


class State(TypedDict):
    question: str
    answer: str
    docs: List[Any]


class EngineGraph:
    def __init__(self):
        self.retrieval_agent = RetrievalAgent()
        self.answer_agent = AnswerAgent()
        self.sql_agent = SqlAgent()

    def retrieve_node(self, state: State):
        docs = self.retrieval_agent.run(
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

        # Rebuild no RAG após mutation
        rebuild_vectorstore_from_sql()

        return {"answer": sql_result}

    def needs_sql(self, question: str) -> bool:
        triggers = [
            # CREATE
            "adicionar",
            "adiciona",
            "adicionae",
            "colocar",
            "coloque",
            "inserir",
            "insira",
            "insert",
            "criar",
            "crie",
            "cadastrar",
            "cadastre",
            "registrar",
            "registre",
            "add",
            "append",
            "incluir",
            "inclua",
            # UPDATE
            "atualizar",
            "atualize",
            "update",
            "editar",
            "edite",
            "modificar",
            "modifique",
            "alterar",
            "altere",
            "mudar",
            "trocar",
            "corrigir",
            "corrija",
            "ajustar",
            "ajuste",
            "setar",
            "set",
            "patch",
            # DELETE
            "deletar",
            "delete",
            "deleta",
            "remover",
            "remova",
            "excluir",
            "exclua",
            "apagar",
            "apague",
            "remove",
            "rm",
            "clear",
            "drop",
        ]

        q = question.lower()
        return any(t in q for t in triggers)

    def build_graph(self):
        graph = StateGraph(State)

        graph.add_node("retrieve", self.retrieve_node)
        graph.add_node("answer", self.answer_node)
        graph.add_node("sql", self.sql_node)

        graph.set_entry_point("retrieve")

        # Sempre → retrieve → answer
        graph.add_edge("retrieve", "answer")

        # Agora bifurca:
        # se precisa SQL → enviar para sql_node
        # se não precisa → terminar no answer_node
        graph.add_conditional_edges(
            "answer",
            lambda state: "sql" if self.needs_sql(state["question"]) else "final",
            {
                "sql": "sql",
                "final": "answer",
            },
        )

        graph.set_finish_point("answer")

        conn = sqlite3.connect("state.db", check_same_thread=False)
        checkpointer = SqliteSaver(conn)
        return graph.compile(
            checkpointer=checkpointer,
        )
