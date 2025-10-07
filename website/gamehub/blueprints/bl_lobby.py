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
from flask.typing import ResponseReturnValue

from website.gamehub.controllers.activities import get_activity
from website.gamehub.controllers.rooms import add_room, get_room

from ..blueprints.auth import manage_cookie_policy, username_required
from ..controllers.rooms import get_all_rooms
from ..model.Room import Room
from ..utils import set_menu

bp = Blueprint('bl_lobby', __name__)


@bp.route('/', methods=('GET',))
def lobby() -> str:
    mc: dict[str, str]  = set_menu('lobby')
    return render_template(
        'lobby/lobby.html',
        mc=mc,
        rooms=[
            {
                'room_id': k,
                'activity': get_activity(r['activity']),
                'members': r['members'].values(),
                'password': True if r['password'] else None,
            }
            for k, r in get_all_rooms().items()
        ],
    )


@bp.route('/room/<string:room_id>', methods=('GET',))
@username_required
def join_room(room_id: str) -> ResponseReturnValue:
    room = get_room(room_id)
    print('Join room: ', room_id, room)
    if room is None:
        return Response(status=404)
    if room['password']:
        # To Do: Add handling room psswd
        return 'Room is protected by password'
    session['room'] = room_id
    mc: dict[str, str] = set_menu(f'room {room_id}')
    return render_template(
        f'activities/{room["activity"]}.html', mc=mc, room=room
    )


@bp.route('/room', methods=('POST', 'GET'))
@username_required
def create_room() -> ResponseReturnValue:
    if request.method == 'POST':
        data = request.get_json()
        room = Room(
            data.get('activity', 'chat'),
            data.get('password', None),
        )
        if add_room(room):
            session['room'] = room.room_id
            print('Create room: ', room.room_id, room)
            return Response(status=201)
    elif request.method == 'GET':
        if session.get('room'):
            return redirect(
                url_for('bl_lobby.join_room', room_id=session['room']), 302
            )
        else:
            return redirect(url_for('bl_lobby.lobby'), 302)
    return Response(status=404)


@bp.route('/about', methods=('GET', 'POST'))
@manage_cookie_policy
def about():
    mc = set_menu('about')
    # bar = create_plot()
    bar = None
    return render_template('lobby/about.html', mc=mc, plot=bar)


@bp.route('/privacy-notice', methods=('GET', 'POST'))
def privacy():
    mc = set_menu('')
    return render_template('lobby/privacy-notice.html', mc=mc)


@bp.route('/terms-of-service', methods=('GET', 'POST'))
def terms_of_service():
    mc = set_menu('')
    return render_template('lobby/terms-of-service.html', mc=mc)


# MANAGE sitemap and robots calls
# These files are usually in root, but for Flask projects must
# be in the static folder
@bp.route('/robots.txt')
@bp.route('/sitemap.xml')
def static_from_root() -> Response:
    if path_dir := current_app.static_folder:
        return send_from_directory(path_dir, request.path[1:])
    return Response(status=404)


# import plotly
# import plotly.graph_objs as go

# import pandas as pd
# import numpy as np
# import json


# def create_plot():
#     generator = np.random.default_rng(42)
#     n = 40
#     x = np.linspace(0, 1, n)
#     y = generator.random(n)
#     df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
#     data = [
#         go.Bar(
#             x=df['x'],  # assign x as the dataframe column 'x'
#             y=df['y'],
#         )
#     ]
#     graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#     return graph_json
