import dataclasses
from typing import Any

from flask import Response, session
from flask_socketio import emit, join_room, leave_room, send

from website.gamehub.controllers.rooms import delete_room, update_room
from website.gamehub.extensions import socketio
from website.gamehub.model.room import Room
from website.gamehub.model.user import User

from .auth import room_access


@socketio.on('message')
@room_access
def handle_message(user: User, room: Room, message: str) -> Response:
    send(f'{user.username}: {message}', to=room.room_id)
    return Response(status=200)


@socketio.on('connect')
@room_access
def handle_connect(user: User, room: Room) -> Response:
    join_room(room.room_id)
    data = {
        'username': user.username,
        'members': get_members(room),
    }
    emit('game_stop', to=room.room_id)
    emit('new_connection', data, to=room.room_id)
    return Response(status=200)


@socketio.on('disconnect')
@room_access
def handle_disconnect(user: User, room: Room) -> Response:
    room['members'].pop((user.user_id, user.username))
    session.pop('room')
    data = {
        'username': user.username,
        'members': get_members(room),
    }
    emit('game_stop', to=room.room_id)
    emit('lost_connection', data, to=room.room_id)
    leave_room(room.room_id)
    _ = (
        delete_room(room.room_id)
        if not bool(room['members']) and not room.is_dedicated
        else update_room(room)
    )
    return Response(status=200)


def get_members(room: Room) -> list[dict[str, Any]]:
    return [dataclasses.asdict(m) for m in room.members.values()]
