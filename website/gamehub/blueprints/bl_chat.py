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
    username = user.username

    join_room(room.room_id)
    emit('new_connection', username, to=room.room_id)
    return Response(status=200)


@socketio.on('disconnect')
@room_access
def handle_disconnect(user: User, room: Room) -> Response:
    room['members'].pop((user.user_id, user.username))
    session.pop('room')
    emit('lost_connection', user.username, to=room.room_id)
    leave_room(room.room_id)
    _ = delete_room(room.room_id) if not bool(room['members']) else update_room(room)
    return Response(status=200)
