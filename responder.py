"""Template-based response generator for classified messages."""

from classifier import Category

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
