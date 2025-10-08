from typing import Any


def validate_username(username: Any) -> bool:
    if username is not None and all((isinstance(username, str), len(username) > 3)):
        return True
    return False
