import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class User:
    username: str
    user_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    points: int = field(default=0, kw_only=True)
    is_registered: bool = field(default=False, kw_only=True)
    is_ready: bool = field(default=False, kw_only=True)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)
