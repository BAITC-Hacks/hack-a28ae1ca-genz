"""Template-based and LLM-based response generator for classified messages."""

from classifier import Category
from llm_client import call_llm

RESPONSE_TEMPLATES: dict[Category, str] = {
    "справка": "Для получения информации обратитесь в деканат или справочную службу.",
    "жалоба": "Обращение подготовлено для передачи ответственному сотруднику.",
    "другое": "Ваше обращение зарегистрировано. Ожидайте ответа.",
}


def generate_response(category: Category, message: str) -> str:
    """Generate a response based on the classified category.

    Args:
        category: The classification category.
        message: The original message (for potential context extraction).

    Returns:
        A response string in Russian.
    """
    return RESPONSE_TEMPLATES.get(category, RESPONSE_TEMPLATES["другое"])


def validate_response(response: str) -> bool:
    """Check if a response is valid (non-empty and appears to be Russian).

    Args:
        response: The response string to validate.

    Returns:
        True if the response is valid.
    """
    if not response or not response.strip():
        return False
    has_cyrillic = bool(__import__("re").search(r"[а-яА-ЯёЁ]", response))
    return has_cyrillic


RESPONSE_SYSTEM_PROMPT = """You are a helpful assistant generating responses to Russian student messages.

Rules:
- All responses must be in Russian
- Keep responses short, polite, neutral, and useful
- Never hallucinate facts (no office numbers, URLs, names, hours)
- For complaints (жалоба): use phrasing like "Обращение подготовлено для передачи ответственному сотруднику"
- For information requests (справка): provide general guidance without specific details
- For other (другое): acknowledge the message and indicate it's registered"""

RESPONSE_PROMPT = """Generate a response to this student message.

Category: {category}
Message: {message}

Respond with ONLY the response text in Russian. No quotes, no explanation."""


def generate_response_with_llm(category: Category, message: str) -> str:
    """Generate a response using LLM with fallback to template.

    Args:
        category: The classification category.
        message: The original message.

    Returns:
        A response string in Russian.
    """
    try:
        prompt = RESPONSE_PROMPT.format(category=category, message=message)
        response = call_llm(prompt, system=RESPONSE_SYSTEM_PROMPT)

        if response and validate_response(response):
            return response

    except (ValueError, ImportError):
        pass

    return generate_response(category, message)
