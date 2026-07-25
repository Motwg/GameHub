import json
import logging
from typing import Literal

from flask import Flask
from redis import Redis

from website.gamehub.encoder import CustomJSONProvider

from .errorhandlers import error_404, error_500
from .extensions import session, socketio
from .jinjafilters import display_error, display_message, slugify


def create_app(mode: Literal['test', 'prod'] = 'prod') -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.logger.setLevel(logging.DEBUG)
    if mode == 'prod':
        _ = app.config.from_file('../prod-config.json', load=json.load)

        app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379)
    else:
        _ = app.config.from_file('../test-config.json', load=json.load)
    if app.config.get('SESSION_TYPE') is not None:
        session.init_app(app)
    socketio.init_app(
        app,
        cors_allowed_origins='*',
        manage_session=app.config.get('SESSION_TYPE') is None,
        json=CustomJSONProvider(app),
    )

    with app.app_context():
        # Add Blueprints
        from .blueprints import auth, bl_lobby

        app.register_blueprint(auth.bp)
        app.register_blueprint(bl_lobby.bp)

        from .blueprints import bl_activity, bl_cah, bl_chat

        app.register_error_handler(404, error_404)
        app.register_error_handler(500, error_500)
        # jinja filters
        app.jinja_env.filters['slugify'] = slugify
        app.jinja_env.filters['displayError'] = display_error
        app.jinja_env.filters['displayMessage'] = display_message
    return app
