import dataclasses

from website.gamehub.db import db
from website.gamehub.model.room import Room


def add_room(room: Room) -> bool:
    if get_room(room.room_id) == room:
        return False
    while room.room_id in db.rooms:
        room.new_id()
    db.rooms[room.room_id] = room
    return True


def delete_room(room_id: str) -> bool:
    try:
        _ = db.rooms.pop(room_id)
    except KeyError:
        return False
    except Exception:
        raise
    else:
        return True


def update_room(room: Room) -> bool:
    try:
        room_reference = db.rooms[room.room_id]
        for field in dataclasses.fields(Room):
            setattr(room_reference, field.name, getattr(room, field.name))
    except KeyError:
        return False
    except Exception:
        raise
    else:
        return True


def get_room(room_id: str) -> Room | None:
    return db.rooms.get(room_id, None)


def get_all_rooms() -> dict[str, Room]:
    return db.rooms
