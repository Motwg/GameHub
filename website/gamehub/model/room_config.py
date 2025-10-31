from collections.abc import Generator
from dataclasses import dataclass
from typing import Deque, Never

from website.gamehub.model.user import User

T: type = 

@dataclass(slots=True)
class RoomConfig:
    status: str

@dataclass(slots=True)
class CahConfig(RoomConfig)
    queue: Deque[User]
    black: Generator[str, T, Never]
    white: Generator[str, T, Never]
