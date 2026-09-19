import json


def parse_json_response(content: str) -> dict:
    normalized = content.strip()
    if normalized.startswith("```"):
        normalized = normalized.removeprefix("```").removeprefix("json").strip()
        normalized = normalized.removesuffix("```").strip()

    try:
        return json.loads(normalized)
    except json.JSONDecodeError:
        start = normalized.find("{")
        end = normalized.rfind("}")
        if start < 0 or end <= start:
            raise
        return json.loads(normalized[start : end + 1])
