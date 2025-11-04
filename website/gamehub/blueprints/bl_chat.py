from flask import Response
from flask_socketio import send

from website.gamehub.extensions import socketio
from website.gamehub.model.room import Room
from website.gamehub.model.user import User

from .auth import room_access


@socketio.on('message')
@room_access
def handle_message(user: User, room: Room, message: str) -> Response:
    send(f'{user.username}: {message}', to=room.room_id)
    return Response(status=200)
