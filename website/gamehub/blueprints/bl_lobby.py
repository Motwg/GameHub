from collections import OrderedDict

from flask import (
    Blueprint,
    Response,
    current_app,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask.typing import ResponseValue

from website.gamehub.blueprints.auth import login_required, manage_cookie_policy
from website.gamehub.controllers.activities import get_activity
from website.gamehub.controllers.rooms import add_room, get_all_rooms, get_room, update_room
from website.gamehub.model.room import Room
from website.gamehub.model.user import User
from website.gamehub.utils import set_menu

bp = Blueprint('bl_lobby', __name__)


@bp.route('/', methods=('GET',))
def lobby() -> str:
    mc: dict[str, str] = set_menu('lobby')
    return render_template(
        'lobby/lobby.html',
        mc=mc,
        rooms=[
            {
                'room_id': k,
                'activity': get_activity(r.activity),
                'members': map(str, r.members.keys()),
                'password': bool(r.password),
            }
            for k, r in get_all_rooms().items()
        ],
    )


@bp.route('/room/<string:room_id>', methods=('GET',))
@login_required
def join_room(user: User, room_id: str) -> ResponseValue:
    room = get_room(room_id)
    if room is None:
        return Response(status=404)
    if room.password:
        # TODO: Add handling room psswd
        return 'Room is protected by password'
    room.members[(str(user.user_id), user.username)] = user
    if not update_room(room):
        _ = room.members.pop((str(user.user_id), user.username))
        return Response(status=404)
    session['room'] = room_id
    mc: dict[str, str] = set_menu(f'room {room_id}')
    return render_template(f'activities/{room.activity}.html', mc=mc, room=room)


@bp.route('/room', methods=('POST', 'GET'))
@login_required
def create_room(user: User) -> ResponseValue:
    if request.method == 'POST':
        data = request.get_json()
        room = Room(
            data.get('activity', 'chat'),
            data.get('password', None),
            members=OrderedDict({(str(user.user_id), user.username): user}),
        )
        if add_room(room):
            session['room'] = room.room_id
            return Response(status=201)
    elif request.method == 'GET':
        if session.get('room'):
            return redirect(url_for('bl_lobby.join_room', room_id=session['room']), 302)
        return redirect(url_for('bl_lobby.lobby'), 302)
    return Response(status=404)


@bp.route('/about', methods=('GET', 'POST'))
@manage_cookie_policy
def about() -> str:
    mc = set_menu('about')
    bar = None
    return render_template('lobby/about.html', mc=mc, plot=bar)


@bp.route('/privacy-notice', methods=('GET', 'POST'))
def privacy() -> str:
    mc = set_menu('')
    return render_template('lobby/privacy-notice.html', mc=mc)


@bp.route('/terms-of-service', methods=('GET', 'POST'))
def terms_of_service() -> str:
    mc = set_menu('')
    return render_template('lobby/terms-of-service.html', mc=mc)


@bp.route('/robots.txt')
@bp.route('/sitemap.xml')
def static_from_root() -> Response:
    if path_dir := current_app.static_folder:
        return send_from_directory(path_dir, request.path[1:])
    return Response(status=404)
