from typing import Any
import uuid


def generate_unique_id() -> str:
    """Generate a unique identifier."""
    return str(uuid.uuid4())


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
