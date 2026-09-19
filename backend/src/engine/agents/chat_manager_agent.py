from engine.tools.sql_tools import criar_ou_buscar_chat_tool, salvar_turno_conversa_tool
from utils.json_response import parse_json_response


class ChatManagerAgent:
    def run(self, question: str, answer: str, chat_token: str, chat_history: list):
        title = question.strip().replace("\n", " ")[:80] or "Novo chat"
        chat_result = parse_json_response(
            criar_ou_buscar_chat_tool.invoke(
                {"titulo": title, "chat_token": chat_token}
            )
        )
        token = chat_result.get("chat_token") or chat_result.get("token")
        if not token:
            raise ValueError("A persistência não retornou um token de chat válido.")

        save_result = parse_json_response(
            salvar_turno_conversa_tool.invoke(
                {"chat_token": token, "question": question, "answer": answer}
            )
        )
        if save_result.get("status") == "erro":
            raise ValueError(save_result.get("message", "Não foi possível salvar o turno."))
        return token
