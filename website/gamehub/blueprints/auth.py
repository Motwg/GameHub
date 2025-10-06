import functools
import os

from flask import (
    Blueprint,
    Response,
    current_app,
    flash,
    g,
    redirect,
    request,
    session,
    url_for,
)

from ..model.User import User
from ..validators.auth import validate_username

bp = Blueprint('auth', __name__, url_prefix='/auth')


# IMPORTANT! Called for every request
@bp.before_app_request
def pre_operations():
    # static requests bypass
    if request.endpoint == 'static':
        return

    # REDIRECT http -> https
    if 'DYNO' in os.environ:
        current_app.logger.critical('DYNO ENV !!!!')
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

    g.policyCode = -1  # SET DEFAULT INDEPENDENTLY TO WRAPPER
    policy_code = session.get('cookie-policy')
    # print(f'AUTH: policy_code = {policy_code}')
    # possible values Null -> no info, 0 -> Strict, 1 -> Minimal,
    #                                 2 -> Analysis, 3 -> All
    if policy_code is not None:
        g.policyCode = policy_code


# WRAPPER FOR COOKIE SETTINGS
def manage_cookie_policy(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        g.showCookieAlert = False  # DEFAULT
        if g.policyCode is None or g.policyCode == -1:
            g.showCookieAlert = True

        return view(**kwargs)

    return wrapped_view


def username_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user' not in session:
            flash('miss_username')
            return redirect(url_for('bl_lobby.lobby'), 302)

        return view(*args, **kwargs)

    return wrapped_view


@bp.route('/login', methods=('POST',))
def login():
    username = request.get_json().get('username')
    print(User(username)['username'])
    if validate_username(username):
        user = session.get('user', User(username))
        user['username'] = username
        session['user'] = user
        return Response(status=200)
    return Response(status=401)


@bp.route('/ajcookiepolicy/', methods=('GET', 'POST'))
def ajcookiepolicy():
    # DECIDE COOKIE PREFERENCE STRATEGY
    if request.method == 'POST':
        data = request.json
        btn_name = data['btnselected']
        checkbox_analysis = data['checkboxAnalysis']
        checkbox_necessary = data['checkboxNecessary']
        if btn_name == 'btnAgreeAll':
            session['cookie-policy'] = 3
        elif btn_name == 'btnAgreeEssential':
            session['cookie-policy'] = 1
        elif btn_name == 'btnSaveCookieSettings':
            session['cookie-policy'] = 0  # default
            if checkbox_necessary and not checkbox_analysis:
                session['cookie-policy'] = 1
            elif checkbox_analysis and not checkbox_necessary:
                # never happens if main checkbox disabled!
                session['cookie-policy'] = 2
            elif checkbox_necessary and checkbox_analysis:
                session['cookie-policy'] = 3

    return Response(status=204)
