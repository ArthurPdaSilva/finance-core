from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from engine.prompts import SQL_AGENT_PROMPT
from engine.tools.sql_tools import (
    add_registro_tool,
    add_usuario_tool,
    alterar_usuario_do_registro_por_nome_tool,
    atualizar_registro_por_nome_tool,
    atualizar_usuario_por_nome_tool,
    remover_registro_por_nome_tool,
    remover_usuario_por_nome_tool,
)
from utils.llm import make_llm


class SqlAgent:
    def __init__(self):
        self.llm = make_llm()

        self.agent = create_agent(
            model=self.llm,
            tools=[
                add_registro_tool,
                atualizar_registro_por_nome_tool,
                alterar_usuario_do_registro_por_nome_tool,
                remover_registro_por_nome_tool,
                add_usuario_tool,
                atualizar_usuario_por_nome_tool,
                remover_usuario_por_nome_tool,
            ],
        )

    def run(self, question: str, chat_history: list):
        system_prompt = SQL_AGENT_PROMPT.replace("{{user_input}}", question)

        result = self.agent.invoke(
            {
                "messages": [
                    *chat_history,
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=question),
                ]
            }
        )

        return result["messages"][-1].content
