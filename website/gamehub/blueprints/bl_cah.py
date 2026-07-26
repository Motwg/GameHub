from typing import TYPE_CHECKING

from flask import Response
from flask_socketio import emit

from website.gamehub.extensions import socketio
from website.gamehub.model.room import Room
from website.gamehub.model.room_controllers import CahController, UserId
from website.gamehub.model.user import User

from .auth import in_game


@socketio.on('get_turn_data')
@in_game(CahController)
def handle_get_turn_data(user: User, _: Room, controller: CahController, sid: str) -> Response:
    data = {
        'cards': controller.cards[(user.user_id, user.username)],
        'black_card': controller.black_card,
        'gaps': controller.gaps,
        'master': controller.cah_master == (user.user_id, user.username),
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
            [controller.cards[member][idx] for idx in controller.confirmed_cards.get(member, [])]
            for member in controller.queue
            if member != controller.cah_master
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
    if controller.status == 'awaiting_winner' \
        and controller.cah_master == (user.user_id, user.username):

        controller.status = 'winner_check'
        winner = None
        confirmed_cards: dict[UserId, list[str]] = {}
        for member, confirmed_idx in controller.confirmed_cards.items():
            confirmed_cards[member] = [controller.cards[member][idx] for idx in confirmed_idx]
            if confirmed_cards[member] == cards:
                winner = member
        if winner in room.members:
            room.members[winner].points += 1
            controller.end_round(confirmed_cards)
            controller.prepare_next_round()
            emit('refresh_members', room.get_members(), to=room.room_id)
            emit('next_round', to=room.room_id)
            return Response(status=200)
        controller.status = 'awaiting_winner'
    return Response(status=200)
