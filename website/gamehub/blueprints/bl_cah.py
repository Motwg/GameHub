from typing import TYPE_CHECKING

from flask import Response
from flask_socketio import emit

from website.gamehub.blueprints.bl_activity import get_members
from website.gamehub.extensions import socketio
from website.gamehub.model.room import Room
from website.gamehub.model.room_controllers import CahController
from website.gamehub.model.user import User

from .auth import in_game

if TYPE_CHECKING:
    import uuid


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
        controller.confirmed_cards[(user.user_id, user.username)] = cards

        confirmed_cards = [
            [controller.cards[m][idx] for idx in controller.confirmed_cards.get(m, [])]
            for m in controller.queue
            # TODO: uncomment
            # if m != controller.cah_master
        ]

        if all(len(c) == controller.gaps for c in confirmed_cards):
            emit('cards_confirmed', confirmed_cards, to=room.room_id)
            controller.status = 'awaiting_winner'
            emit('chose_winner', to=room.members[controller.cah_master].sid)
    return Response(status=200)


@socketio.on('winner_chosen')
@in_game(CahController)
def handle_winner_chosen(
    user: User,
    room: Room,
    controller: CahController,
    cards: list[str],
) -> Response:
    if controller.status == 'awaiting_winner':
        controller.status = 'winner_check'
        if controller.cah_master == (user.user_id, user.username):
            winner = None
            confirmed_cards: dict[tuple[uuid.UUID, str], list[str]] = {}
            for m, m_cards in controller.cards.items():
                confirmed_cards[m] = [m_cards[idx] for idx in controller.confirmed_cards[m]]
                if confirmed_cards[m] == cards:
                    winner = m
            if winner in room.members:
                room.members[winner].points += 1
                controller.end_round(confirmed_cards)
                controller.prepare_next_round()
                emit('refresh_members', get_members(room), to=room.room_id)
                emit('next_round', to=room.room_id)
                return Response(status=200)
        controller.status = 'awaiting_winner'
    return Response(status=200)
