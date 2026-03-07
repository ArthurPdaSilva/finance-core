import json

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from engine.prompts import CHAT_MANAGER_PROMPT
from engine.tools.sql_tools import criar_ou_buscar_chat_tool, salvar_turno_conversa_tool
from utils.llm import make_llm


class ChatManagerAgent:
    def __init__(self):
        self.llm = make_llm()

        self.agent = create_agent(
            model=self.llm,
            tools=[
                criar_ou_buscar_chat_tool,
                salvar_turno_conversa_tool,
            ],
        )

    def run(self, question: str, answer: str, chat_id, chat_history: list):
        user_input = f"Chat ID atual: {chat_id if chat_id else 'Nulo'}. Pergunta: {question}. Resposta: {answer}."

        system_prompt = CHAT_MANAGER_PROMPT.replace("{{user_input}}", user_input)

        result = self.agent.invoke(
            {
                "messages": [
                    *chat_history,
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=question),
                    AIMessage(content=answer),
                ]
            }
        )

        final_content = result["messages"][-1].content

        # transforma em dict
        data = json.loads(final_content)

        return data["chat_id"]
