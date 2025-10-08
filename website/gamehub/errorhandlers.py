from flask import render_template, g


# error handlers
def error_404(e: Exception):
    # mc is for the menu highlighting, which in this case should not be set
    print(f'Error 404: {e}')
    return render_template('error-pages/error404.html', mc='', g=g), 404


def error_500(e: Exception):
    # mc is for the menu highlighting, which in this case should not be set
    print(f'Error 505: {e}')
    return render_template('error-pages/error500.html', mc='', g=g), 500
