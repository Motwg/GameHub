from website.gamehub.model.Room import Room
from website.gamehub.db import db


def add_room(room: Room) -> bool:
    while room.room_id in db.rooms.keys():
        print(f'Id needs to be changed from {room.room_id}')
        room.new_id()
        print(f'Changing to {room.room_id}')
    db.rooms[room.room_id] = room
    return True


def delete_room(room_id: str) -> bool:
    try:
        _ = db.rooms.pop(room_id)
        return True
    except KeyError:
        return False


def update_room(room: Room) -> bool:
    try:
        db.rooms[room.room_id] = room
        return True
    except KeyError:
        return False


def get_room(room_id: str) -> Room | None:
    return db.rooms.get(room_id, None)


def get_all_rooms() -> dict[str, Room]:
    return db.rooms
