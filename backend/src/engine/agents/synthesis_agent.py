from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from engine.prompts import SYNTHESIS_AGENT_PROMPT
from utils.llm import make_llm


class SynthesisAgent:
    def __init__(self):
        self.llm = make_llm()
        self.agent = create_agent(model=self.llm, tools=[])

    def run(self, answer: list[str]):
        context = "\n\n".join(answer)

        system_prompt = SYNTHESIS_AGENT_PROMPT.replace("{{context}}", context)

        result = self.agent.invoke(
            {
                "messages": [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=context),
                ]
            }
        )

        return result["messages"][-1].content
