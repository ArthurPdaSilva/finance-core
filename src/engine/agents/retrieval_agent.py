import json

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from engine.tools.search_finance import search_finance_tool
from utils.llm import make_llm


class RetrievalAgent:
    def __init__(self):
        self.llm = make_llm()

        self.system_message = SystemMessage(
            content="""
                Você é um agente responsável APENAS por recuperar documentos financeiros.

                REGRAS:
                - Use obrigatoriamente a ferramenta de busca.
                - NÃO responda perguntas.
                - NÃO interprete dados.
                - Retorne SOMENTE os documentos encontrados.
                - Se nada for encontrado, retorne uma lista vazia.
                """
        )

        self.agent = create_agent(model=self.llm, tools=[search_finance_tool])

    def run(self, query: str):
        result = self.agent.invoke(
            {
                "messages": [
                    self.system_message,
                    HumanMessage(content=query),
                ]
            }
        )

        for msg in result["messages"]:
            if isinstance(msg, ToolMessage) and msg.name == "search_finance_tool":
                return json.loads(msg.content)
        return []
