from langchain_core.messages import AIMessage, HumanMessage


def parse_history(chat_history: list[str]):
    parsed = []

    last_messages = chat_history[-6:]

    for msg in last_messages:
        sender, text = msg.split(": ", 1)

        if sender == "user":
            parsed.append(HumanMessage(content=text))
        else:
            parsed.append(AIMessage(content=text))

    return parsed
