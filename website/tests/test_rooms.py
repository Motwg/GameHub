import unittest
from typing import override

from website.gamehub.controllers.rooms import (
    add_room,
    delete_room,
    get_all_rooms,
    get_room,
    update_room,
)
from website.gamehub.db import db
from website.gamehub.model.Room import Room


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

    def test_get_room(self) -> None:
        raise NotImplementedError

    def test_add_room(self) -> None:
        room = Room('cah', room_id='test')
        add_room(room)
        # self.assertIsInstance(room, Room)  # noqa: ERA001
        # self.assertTrue(all(isinstance(char, str) for char in chars))  # noqa: ERA001
        # self.assertNotIn('', chars)  # noqa: ERA001
        # self.assertNotIn(None, chars)  # noqa: ERA001
        # self.assertTrue(all([len(char) > 0 for char in chars]))  # noqa: ERA001
        raise NotImplementedError

    def test_delete_room(self) -> None:
        raise NotImplementedError

    def test_update_room(self) -> None:
        raise NotImplementedError


if __name__ == '__main__':
    _ = unittest.main()
