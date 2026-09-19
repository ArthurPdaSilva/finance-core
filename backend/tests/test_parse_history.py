from langchain_core.messages import AIMessage, HumanMessage

from utils.parse_history import parse_history


def test_parse_history_keeps_only_the_last_six_messages():
    history = [
        f"{'user' if index % 2 == 0 else 'assistant'}: message {index}"
        for index in range(8)
    ]

    parsed = parse_history(history)

    assert len(parsed) == 6
    assert all(isinstance(message, HumanMessage) for message in parsed[::2])
    assert all(isinstance(message, AIMessage) for message in parsed[1::2])
