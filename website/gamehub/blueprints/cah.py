from flask import session
from flask_socketio import send, join_room, leave_room

from .auth import username_required
from ..controllers.gamehub import rooms
from ..extensions import socketio


@socketio.on('message')
@username_required
def handle_message(message):
    print(f'Received message: {message}')
    send(f'{session['user']['username']}: {message}', to=session['room'])


@socketio.on('connect')
@username_required
def handle_connect(data):
    print(f'User {session['user']['username']} Connected!', data)
    room = rooms[session['room']]
    user_id, username = session['user']['user_id'], session['user']['username']

    room['members'][user_id] = username
    join_room(session['room'])


@socketio.on('disconnect')
def handle_connect(data):
    print(f'User {session['user']['username']} Disconnected!', data)
    room_id = session['room']
    user_id = session['user']['user_id']
    room = rooms[room_id]

    room['members'].pop(user_id)
    if not bool(room['members']):
        rooms.pop(room_id)
    leave_room(room_id)
    session.pop('room')
