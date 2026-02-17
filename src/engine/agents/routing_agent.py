from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from engine.prompts import ROUTING_AGENT_PROMPT
from utils.llm import make_llm


class RoutingAgent:
    def __init__(self):
        self.llm = make_llm()

        self.system = SystemMessage(content=ROUTING_AGENT_PROMPT)

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
