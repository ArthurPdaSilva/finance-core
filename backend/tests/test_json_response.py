from utils.json_response import parse_json_response


def test_parse_json_response_accepts_markdown_fences_and_surrounding_text():
    content = 'Aqui está:\n```json\n{"intent": "greeting"}\n```'

    assert parse_json_response(content) == {"intent": "greeting"}
