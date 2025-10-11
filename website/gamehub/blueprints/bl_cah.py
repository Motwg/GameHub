from flask import Response, json, jsonify
from flask.typing import ResponseValue
from flask_socketio import emit, send

from website.gamehub.extensions import socketio
from website.gamehub.model.room import Room
from website.gamehub.model.user import User

from .auth import room_access


@socketio.on('ready')
@room_access
def handle_ready(user: User, room: Room, sid: str) -> ResponseValue:
    room.members[(str(user.user_id), user.username)].is_ready = True
    emit('acc_ready', to=sid)
    data = {
        'username': user.username,
        'members': [(m.username, m.is_ready) for m in room.members.values()],
    }
    emit('change_status', data, to=room.room_id)
    return Response(json.dumps({'errors': 'ok'}), status=200, mimetype='application/json')
