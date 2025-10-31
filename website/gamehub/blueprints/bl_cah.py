from collections import deque
from typing import TYPE_CHECKING, Literal

from flask import Response
from flask_socketio import emit

from website.gamehub.blueprints.bl_chat import get_members
from website.gamehub.controllers.cah import get_card_generator
from website.gamehub.controllers.rooms import update_room
from website.gamehub.extensions import socketio
from website.gamehub.model.room import Room
from website.gamehub.model.user import User

from .auth import room_access

if TYPE_CHECKING:
    import uuid


@socketio.on('ready')
@room_access
def handle_ready(user: User, room: Room, sid: str) -> Response:
    user.is_ready = True
    user.sid = sid
    if update_room(room):
        emit('acc_ready', to=sid)
        emit('refresh_members', get_members(room), to=room.room_id)
        if all(m.is_ready for m in room.members.values()):
            init_cah(room)
            if unready_room(room):
                emit('refresh_members', get_members(room), to=room.room_id)
                prepare_next_round(room)
                emit('next_round', to=room.room_id)
    return Response(status=200)


@socketio.on('get_turn_data')
@room_access
def handle_get_turn_data(user: User, room: Room, sid: str) -> Response:
    data = {
        'cards': user.config['cards'],
        'black_card': room.config['black_card'],
        'gaps': room.config['gaps'],
        'is_my_turn': room.config['whose_turn'] == (user.user_id, user.username),
    }
    emit('send_turn_data', data, to=sid)
    return Response(status=200)


@socketio.on('confirm_cards')
@room_access
def handle_confirm_cards(user: User, room: Room, cards: list[int]) -> Response:
    if len(cards) == room.config['gaps']:
        print([user.config['cards'][x] for x in cards])
        user.config['confirmed_cards'] = cards

        confirmed_cards = [
            [m.config['cards'][idx] for idx in m.config.get('confirmed_cards', [])]
            for k, m in room.members.items()
            # TODO: uncomment
            # if k != room.config['whose_turn']
        ]

        if all(len(c) == room.config['gaps'] for c in confirmed_cards):
            print('All cards confirmed: ', confirmed_cards)
            emit('cards_confirmed', confirmed_cards, to=room.room_id)
            emit('chose_winner', to=room.members[room.config['whose_turn']].sid)
    return Response(status=200)


def unready_room(room: Room) -> bool:
    for k in room.members:
        room.members[k].is_ready = False
    return update_room(room)


def init_cah(room: Room) -> None:
    room.config.update(get_card_generator('PL', 'black'))
    room.config.update(get_card_generator('PL', 'white'))
    room.config['queue'] = deque(room.members)
    room.config['status'] = 'start'


def prepare_next_round(room: Room) -> None:
    give_cards(room)
    whose_turn: tuple[uuid.UUID, str] = room.config['queue'].popleft()
    room.config['whose_turn'] = whose_turn
    room.config['queue'].append(whose_turn)

    black_card: str = next(room.config['black'])
    gaps: int = black_card.count('______')
    room.config['black_card'] = black_card
    room.config['gaps'] = gaps if gaps > 0 else 1


def give_cards(room: Room, limit: int = 5) -> None:
    generator = room.config['white']
    for m in room.members.values():
        cards = m.config.get('cards', [])
        while len(cards) < limit:
            cards.append(next(generator))
        m.config['cards'] = cards
