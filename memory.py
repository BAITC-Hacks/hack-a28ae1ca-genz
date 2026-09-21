"""JSON-based memory persistence for processed messages."""

import json
import os
from typing import Any

MEMORY_FILE = "memory.json"


def load_memory(filepath: str = MEMORY_FILE) -> list[dict[str, Any]]:
    """Load memory from a JSON file.

    Args:
        filepath: Path to the memory file.

    Returns:
        A list of processed message records, or empty list if file missing/corrupt.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        return []


def save_memory(records: list[dict[str, Any]], filepath: str = MEMORY_FILE) -> None:
    """Save memory records to a JSON file.

    Args:
        records: List of message records to save.
        filepath: Path to the memory file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def append_record(
    message: str,
    category: str,
    response: str,
    confidence: float,
    filepath: str = MEMORY_FILE,
) -> None:
    """Append a single record to memory.

    Args:
        message: The original message.
        category: The classification category.
        response: The generated response.
        confidence: The classification confidence.
        filepath: Path to the memory file.
    """
    records = load_memory(filepath)
    records.append({
        "message": message,
        "category": category,
        "response": response,
        "confidence": confidence,
    })
    save_memory(records, filepath)
