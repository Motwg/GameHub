import json
from typing import Literal

from flask import Flask

# from flask_session import Session
from .errorhandlers import error_404, error_500
from .extensions import socketio
from .jinjafilters import display_error, display_message, slugify


def create_app(mode: Literal['test', 'prod'] = 'prod') -> Flask:
    if mode == 'prod':
        app = Flask(__name__, instance_relative_config=False)
        _ = app.config.from_file('../prod-config.json', load=json.load)
    else:
        app = Flask(__name__, instance_relative_config=False)
        _ = app.config.from_file('../test-config.json', load=json.load)

    # _ = Session(app)
    socketio.init_app(
        app,
        cors_allowed_origins='*',
        # manage_session=False,
    )
    from .blueprints import bl_activity, bl_cah, bl_chat

    with app.app_context():
        # Add Blueprints
        from .blueprints import bl_lobby

        app.register_blueprint(bl_lobby.bp)

        from .blueprints import auth

        app.register_blueprint(auth.bp)

    # Add error handlers
    app.register_error_handler(500, error_500)
    app.register_error_handler(404, error_404)

    # jinja filters
    app.jinja_env.filters['slugify'] = slugify
    app.jinja_env.filters['displayError'] = display_error
    app.jinja_env.filters['displayMessage'] = display_message

    return app
