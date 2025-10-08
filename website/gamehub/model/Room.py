import random
from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import partial
from string import ascii_uppercase
from typing import Any

from website.gamehub.controllers.cah import get_cards_generators
from website.gamehub.db import LiteralActivities
from website.gamehub.model.User import User


def generate_room_code(length: int) -> str:
    return ''.join(random.choices(ascii_uppercase, k=length))


id_generator = partial(generate_room_code, length=6)


@dataclass(slots=True)
class Room:
    activity: LiteralActivities
    password: None | str = None
    members: dict[str, User] = field(default_factory=dict)
    cards: None | dict[str, Iterator[str]] = field(init=False, default=None)
    room_id: str = field(default_factory=id_generator)

    def __post_init__(self):
        if self.activity == 'cah':
            self.cards = get_cards_generators('PL')

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)

    def new_id(self):
        self.room_id = id_generator()
