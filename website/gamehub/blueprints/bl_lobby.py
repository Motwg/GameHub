from flask import (
    Blueprint, render_template, request, send_from_directory, current_app, flash, Response, session, redirect, url_for
)

from ..controllers.cah import lang_packs, get_cards_generators
from ..controllers.gamehub import activities, rooms, generate_unique_room_code
from ..utils import set_menu
from ..blueprints.auth import manage_cookie_policy, username_required

bp = Blueprint('bl_lobby', __name__)


@bp.route('/', methods=('GET',))
def lobby():
    mc = set_menu('lobby')
    return render_template(
        'lobby/lobby.html',
        mc=mc,
        rooms=[{
            'room_id': k,
            'activity': activities[r['activity']],
            'members': r['members'].values(),
            'password': True if r['password'] else False
        } for k, r in rooms.items()]
    )


@bp.route('/room/<string:room_id>', methods=('GET',))
@username_required
def join_room(room_id):
    room = rooms[room_id]
    print(room_id, room)
    if room['password']:
        return 'Room is protected by password'
    session['room'] = room_id
    mc = set_menu(f'room {room_id}')
    return render_template(
        f'activities/{room['activity']}.html',
        mc=mc,
        room=room
    )


@bp.route('/room', methods=('POST', 'GET'))
@username_required
def create_room():
    if request.method == 'POST':
        data = request.get_json()
        room_id = generate_unique_room_code(6)
        cards = get_cards_generators('PL')

        rooms[room_id] = {
            'members': {},
            'password': data.get('password', False),
            'activity': data.get('activity', 'cah'),
            'cards': {
                'black': cards['black'],
                'white': cards['white']
            },
        }
        session['room'] = room_id
        return Response(status=201)
    elif request.method == 'GET':
        if session.get('room'):
            return redirect(url_for('bl_lobby.join_room', room_id=session['room']), 302)
        else:
            return redirect(url_for('bl_lobby.lobby'), 302)


@bp.route('/about', methods=('GET', 'POST'))
@manage_cookie_policy
def about():
    mc = set_menu('about')
    bar = create_plot()
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
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json


def create_plot():
    generator = np.random.default_rng(42)
    n = 40
    x = np.linspace(0, 1, n)
    y = generator.random(n)
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
    data = [
        go.Bar(
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]
    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json
