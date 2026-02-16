from langchain.agents import create_agent

from utils.llm import make_llm


class AnswerAgent:
    def __init__(self):
        self.llm = make_llm()

        # Nenhuma tool é usada aqui — esse agente só interpreta
        self.agent = create_agent(model=self.llm, tools=[])

    def run(self, question: str, docs: list[str]):
        context = "\n\n".join(docs)

        prompt = f"""
        Você é um assistente financeiro especializado em analisar renda, gastos mensais e dívidas.
        Todas as informações DEVEM vir exclusivamente dos documentos recuperados.

        ### REGRAS OBRIGATÓRIAS
        1. Use APENAS os dados que aparecem nos documentos.
        2. Nunca invente números.
        3. Se faltar informação, diga claramente:
           "Esta informação não está disponível nos documentos recuperados."
        4. Seja direto, preciso e objetivo.
        5. Responda SEMPRE em português do Brasil.
        6. Não misture dados de usuários diferentes.
        7. Não retorne ID's
        8. Não use emojis ou caracteres especiais desnecessários

        ### DOCUMENTOS:
        {context}

        ### PERGUNTA:
        {question}

        ### RESPOSTA:
        """

        result = self.llm.invoke(prompt)
        return result.content
