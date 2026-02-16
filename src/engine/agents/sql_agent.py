from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from engine.tools.sql_tools import (
    add_conta_tool,
    add_divida_tool,
    add_usuario_tool,
    atualizar_conta_por_nome_tool,
    atualizar_divida_por_nome_tool,
    atualizar_usuario_por_nome_tool,
    remover_conta_por_nome_tool,
    remover_divida_por_nome_tool,
    remover_usuario_por_nome_tool,
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
                atualizar_conta_por_nome_tool,
                atualizar_divida_por_nome_tool,
                atualizar_usuario_por_nome_tool,
                remover_conta_por_nome_tool,
                remover_divida_por_nome_tool,
                remover_usuario_por_nome_tool,
            ],
        )

    def run(self, question: str):
        system_prompt = """
        Você é um agente especializado em operações financeiras usando ferramentas Python.
        Você não escreve SQL — somente usa as tools abaixo.

        ### FERRAMENTAS:
        - add_conta(nome, valor, usuario_id=1)
            Adiciona uma nova conta mensal.
        - atualizar_conta_por_nome(nome_atual, novo_nome=None, novo_valor=None, usuario_id=None)
            Atualiza uma conta existente buscando pelo nome, sem expor IDs.
        - remover_conta_por_nome(nome)
            Remove uma conta usando apenas o nome.
        - add_divida(nome, valor_total, parcelas_restantes, usuario_id=1)
            Adiciona uma nova dívida.
        - atualizar_divida_por_nome(nome_atual, novo_nome=None, novo_valor_total=None, novas_parcelas=None, usuario_id=None)
            Atualiza uma dívida existente buscando apenas pelo nome.
        - remover_divida_por_nome(nome)
            Remove uma dívida usando somente o nome.
        - add_usuario(nome, salario)
            Adiciona um novo usuário.
        - atualizar_usuario_por_nome(nome_atual, novo_nome=None, novo_salario=None)
            Atualiza um usuário existente buscando pelo nome.
        - remover_usuario_por_nome(nome)
            Remove um usuário usando apenas o nome.

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
