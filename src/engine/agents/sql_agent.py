from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from engine.tools.sql_tools import (
    add_conta_tool,
    add_divida_tool,
    add_usuario_tool,
    remove_conta_tool,
    remove_divida_tool,
    remove_usuario_tool,
)
from utils.llm import make_llm


class SqlAgent:
    def __init__(self):
        self.llm = make_llm()

        self.agent = create_agent(
            model=self.llm,
            tools=[
                add_conta_tool,
                add_divida_tool,
                add_usuario_tool,
                remove_conta_tool,
                remove_usuario_tool,
                remove_divida_tool,
            ],
        )

    def run(self, question: str):
        system_prompt = """
        Você é um agente especializado em operações financeiras usando ferramentas Python.
        Você não escreve SQL — somente usa as tools abaixo.

        ### FERRAMENTAS:
        - add_conta(nome, valor, usuario_id=1)
        - remove_conta(id)
        - add_divida(nome, valor_total, parcelas_restantes, usuario_id=1)
        - remover_divida(id)
        - add_usuario(nome, salario)
        - remove_usuario(id)

        ### REGRAS:
        - Para contas e dívidas, se usuario_id não for informado, use usuario_id = 1.
        - Para usuários, se não for informado o salario, use salario = 0.
        - Para dívidas sem parcelas: use parcelas_restantes = 1.
        - Nunca invente argumentos.
        - Sempre responda com detalhes do que foi feito.

        """

        result = self.agent.invoke(
            {
                "messages": [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=question),
                ]
            }
        )

        return result["messages"][-1].content
