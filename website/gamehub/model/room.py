import random
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import partial
from string import ascii_uppercase
from typing import Any, Literal

from website.gamehub.model.user import User


def generate_room_code(length: int) -> str:
    return ''.join(random.choices(ascii_uppercase, k=length))


id_generator = partial(generate_room_code, length=6)
LiteralActivities = Literal['cah', 'chat']


@dataclass(slots=True)
class Room:
    activity: LiteralActivities
    password: None | str = None
    members: OrderedDict[tuple[str, str], User] = field(default_factory=OrderedDict)
    room_id: str = field(default_factory=id_generator, kw_only=True)
    is_dedicated: bool = field(default=False, kw_only=True)
    config: dict[str, Any] = field(default_factory=dict, init=False)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def new_id(self) -> None:
        self.room_id = id_generator()
