from collections import deque

from flask import Response
from flask_socketio import emit

from website.gamehub.blueprints.bl_chat import get_members
from website.gamehub.controllers.cah import get_card_generator
from website.gamehub.controllers.rooms import update_room
from website.gamehub.extensions import socketio
from website.gamehub.model.room import Room
from website.gamehub.model.room_controllers import CahController
from website.gamehub.model.user import User

from .auth import in_game, room_access


@socketio.on('ready')
@room_access
def handle_ready(user: User, room: Room, sid: str) -> Response:
    user.is_ready = True
    user.sid = sid
    if update_room(room):
        emit('acc_ready', to=sid)
        emit('refresh_members', get_members(room), to=room.room_id)
        if all(m.is_ready for m in room.members.values()) and unready_room(room):
            init_cah(room)
            emit('refresh_members', get_members(room), to=room.room_id)
            emit('next_round', to=room.room_id)
    return Response(status=200)


@socketio.on('get_turn_data')
@in_game(CahController)
def handle_get_turn_data(user: User, _: Room, controller: CahController, sid: str) -> Response:
    data = {
        'cards': controller.cards[(user.user_id, user.username)],
        'black_card': controller.black_card,
        'gaps': controller.gaps,
        'is_my_turn': controller.cah_master == (user.user_id, user.username),
    }
    emit('send_turn_data', data, to=sid)
    return Response(status=200)


@socketio.on('confirm_cards')
@in_game(CahController)
def handle_confirm_cards(
    user: User,
    room: Room,
    controller: CahController,
    cards: list[int],
) -> Response:
    if len(cards) == controller.gaps:
        print([controller.cards[(user.user_id, user.username)][x] for x in cards])
        controller.confirmed_cards[(user.user_id, user.username)] = cards

        confirmed_cards = [
            [controller.cards[m][idx] for idx in controller.confirmed_cards.get(m, [])]
            for m in controller.queue
            # TODO: uncomment
            # if m != controller.cah_master
        ]

        if all(len(c) == controller.gaps for c in confirmed_cards):
            print('All cards confirmed: ', confirmed_cards)
            emit('cards_confirmed', confirmed_cards, to=room.room_id)
            emit('chose_winner', to=room.members[controller.cah_master].sid)
    return Response(status=200)


def unready_room(room: Room) -> bool:
    for k in room.members:
        room.members[k].is_ready = False
    return update_room(room)


def init_cah(room: Room) -> None:
    room.controller = CahController(
        'init',
        deque(room.members),
        get_card_generator('PL', 'black')['black'],
        get_card_generator('PL', 'white')['white'],
    )
