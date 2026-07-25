import uuid
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass, field

UserId = tuple[uuid.UUID, str]

@dataclass(slots=True)
class RoomController:
    status: str = field(init=False, default='init')


@dataclass(slots=True)
class ChatController(RoomController):
    pass


@dataclass(slots=True)
class CahController(RoomController):
    queue: deque[UserId]
    cah_master: UserId = field(init=False)

    black: Iterator[str]
    white: Iterator[str]
    black_card: str = field(init=False)
    gaps: int = field(init=False)

    cards: dict[UserId, list[str]] = field(init=False, default_factory=dict)
    confirmed_cards: dict[UserId, list[int]] = field(
        init=False,
        default_factory=dict,
    )

    def __post_init__(self) -> None:
        self.prepare_next_round()

    def _next_master(self) -> None:
        self.cah_master = self.queue.popleft()
        self.queue.append(self.cah_master)

    def _give_cards(self, limit: int = 7) -> None:
        generator = self.white
        for m in self.queue:
            while len(self.cards.setdefault(m, [])) < limit:
                self.cards[m].append(next(generator))

    def prepare_next_round(self) -> None:
        self._give_cards()
        self._next_master()

        self.black_card = next(self.black)
        gaps = self.black_card.count('______')
        self.gaps = gaps if gaps > 0 else 1
        self.status: str = 'start_new_round'

    def _remove_cards(self, cards_to_remove: dict[UserId, list[str]]) -> None:
        for m, cards in self.cards.items():
            for to_remove in cards_to_remove.get(m, []):
                cards.remove(to_remove)

    def end_round(self, cards_to_remove: dict[UserId, list[str]]) -> None:
        self._remove_cards(cards_to_remove)
