from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from engine.prompts import SYNTHESIS_AGENT_PROMPT
from utils.llm import make_llm


class SynthesisAgent:
    def __init__(self):
        self.llm = make_llm()
        self.agent = create_agent(model=self.llm, tools=[])

    def run(self, question: str, answer: list[str], chat_history: list):
        context = "\n\n".join(answer)
        system_prompt = SYNTHESIS_AGENT_PROMPT.replace("{{context}}", context)

        result = self.agent.invoke(
            {
                "messages": [
                    *chat_history,
                    SystemMessage(content=system_prompt),
                    AIMessage(content=context),
                    HumanMessage(content=question),
                ]
            }
        )

        return result["messages"][-1].content
