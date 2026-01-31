from flask import Response, g, render_template


# error handlers
def error_404(_: Exception) -> Response:
    return Response(render_template('error-pages/error404.html', mc='', g=g), status=404)


def error_500(_: Exception) -> Response:
    return Response(render_template('error-pages/error500.html', mc='', g=g), status=500)
