from dataclasses import dataclass
from typing import Literal

from website.gamehub.model.Room import Room


@dataclass(slots=True)
class DB:
    activities: dict[Literal['cah', 'chat'], str]
    rooms: dict[str, Room]


db = DB(
    {'cah': 'Cards Against Humanity', 'chat': 'Chat with friends'},
    {
        '14HKE': Room('cah', room_id='14HKE'),
        '13HKE': Room('cah', room_id='13HKE'),
    },
)
