from typing import override
import unittest

from website.gamehub.controllers.rooms import (
    get_room,
    get_all_rooms,
    add_room,
    delete_room,
    update_room,
)
from website.gamehub.db import db
from website.gamehub.model.Room import Room


class TestRoomsCRUD(unittest.TestCase):
    @override
    def setUp(self):
        db.rooms = {
            'chat1': Room('chat', room_id='chat1'),
            'cah12': Room('cah', room_id='cah12'),
            'cah13': Room(
                'cah',
                room_id='cah13',
                password='psswd123',
            ),
        }

    def test_get_room(self):
        raise NotImplemented

    def test_add_room(self):
        room = Room('cah', room_id='test')
        add_room(room)
        # self.assertIsInstance(room, Room)
        # self.assertTrue(all(isinstance(char, str) for char in chars))
        # self.assertNotIn('', chars)
        # self.assertNotIn(None, chars)
        # self.assertTrue(all([len(char) > 0 for char in chars]))
        raise NotImplemented

    def test_delete_room(self):
        # Priori((
        #     np.array([0.333, 0.333, 0.333]),
        #     np.array([0.667, 0.667, 0.667]),
        # ))
        raise NotImplemented

    def test_bayes(self):
        # Posterior((np.array([1, 0, 0.5]), np.array([0, 0.5, 1])))
        raise NotImplemented

if __name__ == '__main__':
    unittest.main()
