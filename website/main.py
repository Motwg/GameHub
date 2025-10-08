#!/usr/bin/env python3
from website.gamehub import create_app
from website.gamehub.extensions import socketio

app = create_app('test')

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
