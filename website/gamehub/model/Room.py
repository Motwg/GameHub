from dataclasses import dataclass


@dataclass(slots=True)
class Room:
    room_id: str
