from typing import Any

from flask import Response, session
from flask_socketio import emit, join_room, leave_room, send

from website.gamehub.controllers.rooms import delete_room, get_room, update_room
from website.gamehub.extensions import socketio
from website.gamehub.model.user import User

from .auth import username_required


@socketio.on('message')
@username_required
def handle_message(message: str) -> Response:
    print(f'Received message: {message}')
    send(f'{session["user"]["username"]}: {message}', to=session['room'])
    return Response(status=200)


@socketio.on('connect')
@username_required
def handle_connect(data: Any) -> Response:
    if room := get_room(session['room']):
        user_id, username = session['user']['user_id'], session['user']['username']

        room['members'][user_id] = User(username)
        if update_room(room):
            join_room(room.room_id)

            print(f'User {username} connected!', data)
            send(f'{username} joined room!', to=room.room_id)
            emit('new_connection', username, to=room.room_id)
            return Response(status=200)
    return Response(status=400)


@socketio.on('disconnect')
def handle_disconnect(data: Any) -> Response:
    room_id = session['room']
    user_id, username = session['user']['user_id'], session['user']['username']
    print(f'User {username} disconnected!', data)

    if room := get_room(room_id):
        room['members'].pop(user_id)
        _ = delete_room(room_id) if not bool(room['members']) else update_room(room)
        send(f'{username} lost connection!', to=room.room_id)
        emit('lost_connection', username, to=room.room_id)
        leave_room(room_id)
        session.pop('room')
        return Response(status=200)
    return Response(status=400)
