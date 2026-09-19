import re

MAX_QUESTION_LENGTH = 4_000
MAX_ANSWER_LENGTH = 12_000

_PROMPT_INJECTION_PATTERNS = (
    re.compile(r"\b(ignore|disregard|forget)\b.{0,40}\b(previous|above|prior)\b", re.I),
    re.compile(r"\b(reveal|show|print|expose)\b.{0,40}\b(system prompt|developer message|instructions)\b", re.I),
    re.compile(r"\b(system prompt|developer message|hidden instructions)\b", re.I),
    re.compile(r"\b(jailbreak|do anything now|dan mode)\b", re.I),
)


class GuardrailViolation(ValueError):
    pass


def validate_question(question: str) -> str:
    normalized = question.strip()
    if not normalized:
        raise GuardrailViolation("A pergunta não pode estar vazia.")
    if len(normalized) > MAX_QUESTION_LENGTH:
        raise GuardrailViolation("A pergunta excede o limite de tamanho permitido.")
    if any(ord(char) < 32 and char not in "\n\t\r" for char in normalized):
        raise GuardrailViolation("A pergunta contém caracteres inválidos.")
    if any(pattern.search(normalized) for pattern in _PROMPT_INJECTION_PATTERNS):
        raise GuardrailViolation(
            "Não posso seguir instruções para revelar ou substituir as regras do sistema."
        )
    return normalized


def validate_answer(answer: str) -> str:
    normalized = answer.strip()
    if not normalized:
        raise GuardrailViolation("Não foi possível gerar uma resposta.")
    if len(normalized) > MAX_ANSWER_LENGTH:
        return normalized[:MAX_ANSWER_LENGTH].rstrip() + "..."
    return normalized
