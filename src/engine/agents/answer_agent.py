from langchain.agents import create_agent

from engine.prompts import GET_ANSWER_AGENT_PROMPT
from utils.llm import make_llm


class AnswerAgent:
    def __init__(self):
        self.llm = make_llm()

        # Nenhuma tool é usada aqui — esse agente só interpreta
        self.agent = create_agent(model=self.llm, tools=[])

    def run(self, question: str, docs: list[str]):
        context = "\n\n".join(docs)

        prompt = GET_ANSWER_AGENT_PROMPT(question=question, context=context)

        result = self.llm.invoke(prompt)
        return result.content
