from flask import Response
from flask_socketio import emit

from website.gamehub.blueprints.bl_chat import get_members
from website.gamehub.controllers.cah import get_card_generator
from website.gamehub.controllers.rooms import update_room
from website.gamehub.extensions import socketio
from website.gamehub.model.room import Room
from website.gamehub.model.user import User

from .auth import room_access


@socketio.on('ready')
@room_access
def handle_ready(user: User, room: Room, sid: str) -> Response:
    user.is_ready = True
    if update_room(room):
        emit('acc_ready', to=sid)
        emit('refresh_members', get_members(room), to=room.room_id)
        if all(m.is_ready for m in room.members.values()):
            start_cah(room)
    return Response(status=200)


@socketio.on('my_cards')
@room_access
def my_cards(user: User, _: Room, sid: str) -> Response:
    emit('my_cards', user.config['cards'], to=sid)
    return Response(status=200)


def unready_room(room: Room) -> bool:
    for k in room.members:
        room.members[k].is_ready = False
    return update_room(room)


def start_cah(room: Room) -> None:
    room.config.update(get_card_generator('PL', 'black'))
    room.config.update(get_card_generator('PL', 'white'))
    if unready_room(room):
        emit('refresh_members', get_members(room), to=room.room_id)
        next_round(room)


def next_round(room: Room) -> None:
    give_cards(room)
    emit('next_round', to=room.room_id)


def give_cards(room: Room, limit: int = 5) -> None:
    generator = room.config['white']
    for m in room.members.values():
        cards = m.config.get('cards', [])
        while len(cards) < limit:
            cards.append(next(generator))
        m.config['cards'] = cards
