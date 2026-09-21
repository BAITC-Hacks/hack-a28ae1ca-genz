"""Request Classifier — main entry point.

Reads messages from messages.txt, classifies each, generates responses,
and prints results to CLI.
"""

from classifier import classify, validate_category
from responder import generate_response, validate_response
from memory import append_record

MESSAGES_FILE = "messages.txt"


def load_messages(filepath: str = MESSAGES_FILE) -> list[str]:
    """Load messages from a text file (one per line).

    Args:
        filepath: Path to the messages file.

    Returns:
        List of non-empty message strings.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
        return []
    except IOError as e:
        print(f"Ошибка чтения файла {filepath}: {e}")
        return []


def process_message(message: str) -> dict:
    """Process a single message through the full pipeline.

    Args:
        message: The input message to classify.

    Returns:
        A dict with keys: message, category, response, confidence, valid.
    """
    if not message or not message.strip():
        return {
            "message": message,
            "category": "другое",
            "response": "",
            "confidence": 0.0,
            "valid": False,
        }

    category, confidence = classify(message)

    if not validate_category(category):
        category = "другое"
        confidence = 0.0

    response = generate_response(category, message)

    if not validate_response(response):
        response = "Ваше обращение зарегистрировано."

    valid = (
        validate_category(category)
        and validate_response(response)
        and 0.0 <= confidence <= 1.0
    )

    return {
        "message": message,
        "category": category,
        "response": response,
        "confidence": confidence,
        "valid": valid,
    }


def main() -> None:
    """Run the classifier pipeline on messages.txt."""
    messages = load_messages()

    if not messages:
        print("Нет сообщений для обработки.")
        return

    print("=" * 60)
    print("Классификатор обращений студентов")
    print("=" * 60)

    for i, message in enumerate(messages, 1):
        result = process_message(message)

        print(f"\n{i}. {result['message']}")
        print(f"   Категория: {result['category']}")
        print(f"   Уверенность: {result['confidence']:.2f}")
        print(f"   Ответ: {result['response']}")
        print(f"   Валидно: {'да' if result['valid'] else 'нет'}")

        if result["valid"]:
            append_record(
                message=result["message"],
                category=result["category"],
                response=result["response"],
                confidence=result["confidence"],
            )

    print("\n" + "=" * 60)
    print("Обработка завершена.")
    print("=" * 60)


if __name__ == "__main__":
    main()
