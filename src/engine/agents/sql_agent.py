from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

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

    def run(self, question: str):
        system_prompt = """
        Você é um agente especializado em operações financeiras usando ferramentas Python.
        Você não escreve SQL — somente usa as tools abaixo.

        ### FERRAMENTAS:
        📌 REGISTROS FINANCEIROS (contas e dívidas unificados)

        add_registro_tool(nome, tipo, usuario_nome=None, valor=None, valor_total=None, parcelas_restantes=None)
            Cria um registro unificado.
            - Para contas → tipo="conta" + valor
            - Para dívidas → tipo="divida" + valor_total + parcelas_restantes

        atualizar_registro_por_nome_tool(nome_atual, novo_nome=None, novo_valor=None,novo_valor_total=None,novas_parcelas=None, novo_tipo=None)
            Atualiza qualquer registro buscando pelo nome.

        remover_registro_por_nome_tool(nome)
            Remove qualquer registro financeiro usando apenas o nome.

        alterar_usuario_do_registro_por_nome_tool(nome, novo_usuario_nome)
            Altera apenas o usuário relacionado ao registro.

        📌 USUÁRIOS

        add_usuario_tool(nome, salario)
            Adiciona um usuário.

        atualizar_usuario_por_nome_tool(...)
            Atualiza dados do usuário pelo nome.

        remover_usuario_por_nome_tool(nome)
            Remove usuário pelo nome.

        ### REGRAS:
        - Para registros: se usuario_nome não for informado → usar usuario_id = 1
        - Para usuários: se salario não for informado → usar salario = 0
        - Para dívidas sem parcelas → usar parcelas_restantes = 1
        - Nunca invente argumentos
        - Sempre usar apenas as tools listadas

  
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
