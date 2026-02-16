from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from utils.llm import make_llm


class RoutingAgent:
    def __init__(self):
        self.llm = make_llm()

        self.system = SystemMessage(
            content="""
            Você é um agente de roteamento.
            Classifique a intenção do usuário entre duas opções:

            - "rag": quando o usuário quer consultar, perguntar, explicar algo ou qualquer assunto que não envolva manipulação de dados financeiros.
                Exemplo: 'Quais usuários estão no banco?'
            - "sql": quando o usuário quer adicionar, atualizar, editar, remover,
              cadastrar ou modificar dados financeiros.
    
            Responda EXATAMENTE em JSON:
            {"intent": "rag"} ou {"intent": "sql"}

            Nada além disso.
            """
        )

        self.agent = create_agent(model=self.llm, tools=[])

    def run(self, query: str):
        resp = self.agent.invoke(
            {
                "messages": [
                    self.system,
                    HumanMessage(content=query),
                ]
            }
        )

        import json

        return json.loads(resp["messages"][-1].content)["intent"]
