from flask import Response, session
from flask_socketio import send

from website.gamehub.extensions import socketio

from .auth import username_required


@socketio.on('ready')
@username_required
def handle_ready() -> Response:
    username, room_id = session['user']['username'], session['room']
    print(f'Player {username} is ready in room {room_id}')
    send(f'Player {username} is ready', to=room_id)
    return Response(status=200)
