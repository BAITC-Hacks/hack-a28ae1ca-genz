"""Rule-based classifier for Russian student messages."""

import re
from typing import Literal

Category = Literal["справка", "жалоба", "другое"]

SPRAVKA_KEYWORDS = [
    "где", "как", "получить", "справк", "парковк", "мест",
    "адрес", "номер", "телефон", "расписан", "время", "документ",
    "информац", "узна", "сказать", "объясн", "помоч",
]

ZHALOBA_KEYWORDS = [
    "очеред", "холодн", "пропал", "проблем", "не работ",
    "сломал", "шум", "гряз", "долго", "ждать", "жалоб",
    "некачествен", "плох", "ужасн", "медленн", "жарк",
    "нет отоплен", "нет вод", "нет свет",
]

FALLBACK_CATEGORY: Category = "другое"


def classify(message: str) -> tuple[Category, float]:
    """Classify a message into a category with confidence score.

    Args:
        message: The input message in Russian.

    Returns:
        A tuple of (category, confidence) where confidence is between 0 and 1.
    """
    if not message or not message.strip():
        return FALLBACK_CATEGORY, 0.0

    normalized = message.lower().strip()

    spravka_matches = sum(1 for kw in SPRAVKA_KEYWORDS if kw in normalized)
    zhaloba_matches = sum(1 for kw in ZHALOBA_KEYWORDS if kw in normalized)

    if spravka_matches == 0 and zhaloba_matches == 0:
        return FALLBACK_CATEGORY, 0.0

    total = spravka_matches + zhaloba_matches

    if spravka_matches > zhaloba_matches:
        return "справка", min(spravka_matches / max(total, 1), 1.0)
    elif zhaloba_matches > spravka_matches:
        return "жалоба", min(zhaloba_matches / max(total, 1), 1.0)
    else:
        return FALLBACK_CATEGORY, 0.5


def validate_category(category: str) -> bool:
    """Check if a category string is valid."""
    return category in {"справка", "жалоба", "другое"}
