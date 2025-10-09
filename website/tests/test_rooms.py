import unittest
from collections import OrderedDict
from typing import override

from website.gamehub.controllers.rooms import (
    add_room,
    delete_room,
    get_all_rooms,
    get_room,
    update_room,
)
from website.gamehub.db import db
from website.gamehub.model.room import Room
from website.gamehub.model.user import User


class TestRoomsCRUD(unittest.TestCase):
    @override
    def setUp(self) -> None:
        db.rooms = {
            'chat1': Room('chat', room_id='chat1'),
            'cah12': Room('cah', room_id='cah12'),
            'cah13': Room(
                'cah',
                room_id='cah13',
                password='test',
            ),
        }
        self.user_id_0, self.user_id_1 = ('31515-2v9uD', 'superTkUser'), ('12vDd3h-5dF', 'verona')
        self.activity, self.room_id, self.password, self.members = (
            'cah',
            'test',
            'psswd',
            {self.user_id_0: User(self.user_id_0), self.user_id_1: User(self.user_id_1)},
        )
        self.room = Room(
            self.activity,
            room_id=self.room_id,
            password=self.password,
            members=self.members,
        )
        self.cards = self.room.cards

    def test_get_room(self):
        room_id = 'chat1'

        room = get_room(room_id)

        assert room is not None
        assert isinstance(room, Room)
        assert room.room_id == room_id
        assert room.activity == 'chat'
        assert room.members == OrderedDict()
        assert room.password is None
        assert room.cards is None

    def test_get_room_no_id(self):
        room = get_room(self.room_id)

        assert room is None

    def test_add_room(self):
        success = add_room(self.room)
        assert success
        got = db.rooms[self.room_id]

        assert len(db.rooms) == 4
        assert isinstance(got, Room)
        assert got.room_id == self.room_id
        assert got.activity == self.activity
        assert got.password == self.password
        assert got.members == self.members
        assert self.user_id_0 in got.members
        assert self.user_id_1 in got.members
        assert got == self.room
        got.password = ''
        assert got.password == self.room.password

    def test_add_room_id_exists(self):
        success = add_room(self.room)
        assert success
        assert len(db.rooms) == 4

        failed = add_room(self.room)
        assert not failed
        assert len(db.rooms) == 4

        got = db.rooms[self.room_id]
        assert got.room_id == self.room_id

    def test_delete_room(self):
        db.rooms[self.room_id] = self.room
        assert len(db.rooms) == 4
        assert self.room_id in db.rooms

        success = delete_room(self.room_id)
        assert success
        assert len(db.rooms) == 3
        assert self.room_id not in db.rooms

        failed = delete_room(self.room_id)
        assert not failed
        assert len(db.rooms) == 3

    def test_update_room(self):
        room_id = 'chat1'
        old_room = db.rooms[room_id]
        new_room = self.room
        new_room.room_id = room_id

        success = update_room(self.room)
        assert success
        room = db.rooms[room_id]

        assert old_room == new_room
        assert room == self.room
        assert old_room.members == self.members
        assert old_room.cards == self.cards

    def test_get_all_rooms(self):
        rooms = get_all_rooms()

        assert isinstance(rooms, dict)
        assert len(rooms) == 3
        assert all(isinstance(r, Room) for r in rooms.values())


if __name__ == '__main__':
    _ = unittest.main()
