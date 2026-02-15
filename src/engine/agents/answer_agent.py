import json

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from engine.tools.search_finance import search_finance_tool
from utils.llm import make_llm


class AnswerAgent:
    def __init__(self):
        self.llm = make_llm()

        # Agora o AnswerAgent usa a ferramenta de busca
        self.agent = create_agent(model=self.llm, tools=[search_finance_tool])

        self.system_message = SystemMessage(
            content="""
            Você é um assistente financeiro especializado em analisar renda, gastos
            mensais e dívidas com base EXCLUSIVA nos documentos recuperados.

            REGRAS OBRIGATÓRIAS:
            1. Use APENAS os dados que aparecem nos documentos recuperados.
            2. Nunca invente números.
            3. Se faltar informação, responda exatamente:
               "Esta informação não está disponível nos documentos recuperados."
            4. Seja direto, preciso e objetivo.
            5. Responda SEMPRE em português do Brasil.
            6. Não misture dados de usuários diferentes.
            7. Não retorne IDs.
            8. Não use emojis ou símbolos desnecessários.
            """
        )

    def run(self, question: str):
        """Executa a pergunta, chamando a tool e interpretando os docs no final."""

        result = self.agent.invoke(
            {
                "messages": [
                    self.system_message,
                    HumanMessage(content=question),
                ]
            }
        )

        # Extrair os documentos retornados pela ferramenta
        docs = []
        for msg in result["messages"]:
            if isinstance(msg, ToolMessage) and msg.name == "search_finance_tool":
                docs = json.loads(msg.content)

        # Se não houver documentos, responder com a regra padrão
        if not docs:
            return "Esta informação não está disponível nos documentos recuperados."

        # Criar o contexto para análise
        context = "\n\n".join(docs)

        # Prompt final para resposta
        final_prompt = f"""
        ### DOCUMENTOS RECUPERADOS:
        {context}

        ### PERGUNTA:
        {question}

        ### RESPOSTA (OBRIGATORIAMENTE seguindo as regras):
        """

        final_answer = self.llm.invoke(final_prompt)
        return final_answer.content
