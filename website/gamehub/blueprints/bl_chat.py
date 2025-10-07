from typing import Any
from flask import session
from flask_socketio import join_room, leave_room, send

from ..controllers.rooms import delete_room, get_room
from ..extensions import socketio
from .auth import username_required
from website.gamehub.controllers.rooms import update_room


@socketio.on('message')
@username_required
def handle_message(message: str):
    print(f'Received message: {message}')
    send(f'{session["user"]["username"]}: {message}', to=session['room'])


@socketio.on('connect')
@username_required
def handle_connect(data: Any):
    if room := get_room(session['room'])
        user_id, username = session['user']['user_id'], session['user']['username']

        room['members'][user_id] = username
        if update_room(room):
            join_room(session['room'])

            print(f'User {session["user"]["username"]} Connected!', data)
            send(f'{session["user"]["username"]} joined room!', to=session['room'])


@socketio.on('disconnect')
def handle_disconnect(data: Any):
    print(f'User {session["user"]["username"]} Disconnected!', data)
    room_id = session['room']
    user_id = session['user']['user_id']
    room = get_room(room_id)

    room['members'].pop(user_id)
    if not bool(room['members']):
        delete_room(room_id)
    leave_room(room_id)
    session.pop('room')
