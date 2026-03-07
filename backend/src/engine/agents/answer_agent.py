from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from engine.prompts import ANSWER_AGENT_PROMPT
from utils.llm import make_llm


class AnswerAgent:
    def __init__(self):
        self.llm = make_llm()

        # Nenhuma tool é usada aqui — esse agente só interpreta
        self.agent = create_agent(model=self.llm, tools=[])

    def run(self, question: str, docs: list[str], chat_history: list):

        context = "\n\n".join(docs)

        system_prompt = ANSWER_AGENT_PROMPT.replace("{{context}}", context).replace(
            "{{user_input}}", question
        )

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
