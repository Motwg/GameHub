from flask import Response, current_app, g, render_template, request

from website.gamehub.extensions import socketio


@socketio.on_error_default
def error_handler(e: BaseException) -> bool:
    current_app.logger.debug('Exception: %s', e)
    current_app.logger.debug('Exception args: %s', e.args)
    current_app.logger.debug(request.event["message"])
    return False

def error_404(_: BaseException) -> Response:
    return Response(render_template('error-pages/error404.html', mc='', g=g), status=404)

def error_500(_: BaseException) -> Response:
    return Response(render_template('error-pages/error500.html', mc='', g=g), status=500)
