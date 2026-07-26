from typing import Any

from flask import Response
from flask_socketio import emit, join_room, leave_room
from werkzeug.exceptions import BadRequest

from website.gamehub.blueprints.auth import room_access, room_connect
from website.gamehub.controllers.rooms import delete_room, unready_room, update_room
from website.gamehub.extensions import socketio
from website.gamehub.model.room import Room
from website.gamehub.model.user import User


@socketio.on('ready')
@room_access
def handle_ready(user: User, room: Room, sid: str) -> Response:
    user.is_ready = True
    user.sid = sid
    if update_room(room):
        emit('acc_ready', to=sid)
        emit('refresh_members', room.get_members(), to=room.room_id)
        if all(m.is_ready for m in room.members.values()) and unready_room(room):
            room.init_controller()
            emit('refresh_members', room.get_members(), to=room.room_id)
            emit('next_round', to=room.room_id)
        return Response(status=200)
    raise BadRequest


@socketio.on('connect')
@room_connect
def handle_connect(user: User, room: Room) -> Response:
    join_room(room.room_id)
    data = {
        'username': user.username,
        'members': room.get_members(),
    }
    emit('game_stop', to=room.room_id)
    emit('new_connection', data, to=room.room_id)
    return Response(status=200)


@socketio.on('disconnect')
@room_access
def handle_disconnect(user: User, room: Room, _: Any) -> Response:
    room['members'].pop((user.user_id, user.username))
    data = {
        'username': user.username,
        'members': room.get_members(),
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
