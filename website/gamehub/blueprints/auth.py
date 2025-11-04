import os
from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

from flask import (
    Blueprint,
    Response,
    abort,
    current_app,
    flash,
    g,
    redirect,
    request,
    session,
    url_for,
)
from flask.typing import ResponseValue

from website.gamehub.controllers.rooms import get_room
from website.gamehub.model.room import Room
from website.gamehub.model.user import User
from website.gamehub.validators.auth import validate_username

bp = Blueprint('auth', __name__, url_prefix='/auth')

P = ParamSpec('P')
T = TypeVar('T')


# IMPORTANT! Called for every request
@bp.before_app_request
def pre_operations() -> ResponseValue | None:
    # static requests bypass
    if request.endpoint == 'static':
        return None
    # REDIRECT http -> https
    if 'DYNO' in os.environ:
        current_app.logger.critical('DYNO ENV !!!!')
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

    g.policyCode = -1  # SET DEFAULT INDEPENDENTLY TO WRAPPER
    policy_code = session.get('cookie-policy')
    # possible values Null -> no info, 0 -> Strict, 1 -> Minimal, 2 -> Analysis, 3 -> All
    if policy_code is not None:
        g.policyCode = policy_code
    return None


# WRAPPER FOR COOKIE SETTINGS
def manage_cookie_policy(view: Callable[P, ResponseValue]) -> Callable[P, ResponseValue]:
    @wraps(view)
    def wrapped_view(*args: P.args, **kwargs: P.kwargs) -> ResponseValue:
        g.showCookieAlert = False  # DEFAULT
        if g.policyCode is None or g.policyCode == -1:
            g.showCookieAlert = True

        return view(*args, **kwargs)

    return wrapped_view


def login_required(
    view: Callable[Concatenate[User, P], ResponseValue],
) -> Callable[P, ResponseValue]:
    @wraps(view)
    def login_view(*args: P.args, **kwargs: P.kwargs) -> ResponseValue:
        try:
            user = User(session['user']['username'], user_id=session['user']['user_id'])
            return view(user, *args, **kwargs)
        except KeyError:
            flash('miss_username')
            return redirect(url_for('bl_lobby.lobby'), 302)

    return login_view


def room_access(
    view: Callable[Concatenate[User, Room, P], ResponseValue],
) -> Callable[P, ResponseValue]:
    @wraps(view)
    @login_required
    def access_view(user: User, *args: P.args, **kwargs: P.kwargs) -> ResponseValue:
        try:
            room = get_room(session['room'])
            if room:
                r_user = room.members[(user.user_id, user.username)]
                return view(r_user, room, *args, **kwargs)
        except KeyError:
            flash('miss_room')
            return redirect(url_for('bl_lobby.lobby'), 302)
        return abort(404)

    return access_view


def in_game(
    room_controller: type[T],
) -> Callable[[Callable[Concatenate[User, Room, T, P], ResponseValue]], Callable[P, ResponseValue]]:
    def inner(
        view: Callable[Concatenate[User, Room, T, P], ResponseValue],
    ) -> Callable[P, ResponseValue]:
        @wraps(view)
        @room_access
        def access_view(user: User, room: Room, *args: P.args, **kwargs: P.kwargs) -> ResponseValue:
            controller = room.controller
            if isinstance(controller, room_controller):
                return view(user, room, controller, *args, **kwargs)
            flash('miss_room')
            return redirect(url_for('bl_lobby.lobby'), 302)

        return access_view

    return inner


@bp.route('/login', methods=('POST',))
def login() -> ResponseValue:
    username = request.get_json().get('username')
    if validate_username(username):
        user = session.get('user', User(username))
        user['username'] = username
        session['user'] = user
        return Response(status=200)
    return Response(status=401)


@bp.route('/ajcookiepolicy/', methods=('GET', 'POST'))
def ajcookiepolicy() -> ResponseValue:
    # DECIDE COOKIE PREFERENCE STRATEGY
    if request.method == 'POST':
        data: dict[str, str | bool] = request.get_json()
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
