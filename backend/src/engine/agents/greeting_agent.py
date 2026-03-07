from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from engine.prompts import GREETINGS_AGENT_PROMPT
from utils.llm import make_llm


class GreetingAgent:
    def __init__(self):
        self.llm = make_llm()

        self.agent = create_agent(
            model=self.llm,
            tools=[],
        )

    def run(self, question: str, chat_history: list):
        system_prompt = GREETINGS_AGENT_PROMPT.replace("{{user_input}}", question)

        result = self.agent.invoke(
            {
                "messages": [
                    *chat_history,
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=question),
                ]
            }
        )

        return result["messages"][-1].content
