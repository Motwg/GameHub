from typing import Any


def validate_username(username: Any) -> bool:
    return bool(username is not None and all((isinstance(username, str), len(username) > 1)))
