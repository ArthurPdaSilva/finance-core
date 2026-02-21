from langchain.agents import create_agent

from engine.prompts import SYNTHESIS_AGENT_PROMPT
from utils.llm import make_llm


class SynthesisAgent:
    def __init__(self):
        self.llm = make_llm()
        self.agent = create_agent(model=self.llm, tools=[])

    def run(self, answer: list[str]):
        context = "\n\n".join(answer)

        prompt = SYNTHESIS_AGENT_PROMPT.replace("{{context}}", context)

        result = self.llm.invoke(prompt)
        return result.content
